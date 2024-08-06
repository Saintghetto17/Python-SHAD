import dataclasses
import io

import pytest

from .git_log import reformat_git_log


@dataclasses.dataclass
class Case:
    log: str
    ans: str


TEST_CASES = [
    Case(
        log='0cd8619f18d8ecad1e5d2303f95ed206c2d6f92b\t'
            'Fri Sep 23 10:59:32 2016 -0700\t'
            'Brett Cannon\t'
            'brettcannon@users.noreply.github.com\t'
            'Update PEP 512 (#107)\n'

            '94dbee096b92f10ab83bbcf88102c6acdc3d76d1\t'
            'Thu Sep 22 12:39:58 2016 +0100\t'
            'Thomas Kluyver\t'
            'takowl@gmail.com\t'
            'Update PEP 517 to use pyproject.toml from PEP 518 (#51)\n',

        ans='0cd8619....................................................Update PEP 512 (#107)\n'
            '94dbee0..................Update PEP 517 to use pyproject.toml from PEP 518 (#51)\n'
    ),
    Case(
        log='3b87611b4b1bbf4b2c36595c894027603beeb570\t'
            'Wed Sep 21 12:27:00 2016 +1000\t'
            'Nick Coghlan\t'
            'ncoghlan@gmail.com\t'
            'PEP 432: Update for C99 initializers (#12)\n'

            'cd22b95028d4802a44b27caa81e533f90fc05f2b\t'
            'Mon Sep 19 12:56:22 2016 -0700\t'
            'Guido van Rossum\t'
            'guido@python.org\t'
            'Fix github URLs\n'

            'e8d0ecf38ffc6af5bd7cb5a61bbaf7ba121d5004\t'
            'Mon Sep 19 12:55:52 2016 -0700\t'
            'Guido van Rossum\t'
            'guido@python.org\t'
            'Skip files with syntax errors\n'

            '2a4515c42998817a7d9be89df266863576da3f2d\t'
            'Mon Sep 19 12:42:18 2016 -0700\t'
            'Roy Williams\t'
            'roy.williams.iii@gmail.com\t'
            'Change emoji used in PEP 505 (#106)\n'

            'a116d3d13c9b15c15c9fb5323ac0f419d68cfda3\t'
            'Mon Sep 19 13:52:01 2016 +0300\t'
            'Ville Skyttä\t'
            'ville.skytta@iki.fi\t'
            'PEP 3333: Fix links to web programming topic and CGI spec (#104)\n'

            'af6fab3d428fbb8b9b533b4896b48f362783c07b\t'
            'Fri Sep 16 16:06:04 2016 -0400\t'
            'Ned Deily\t'
            'nad@python.org\t'
            'Update list of PEPs as implemented in 3.6.0b1\n'

            '00d5884ed64bc681f428ad70a01c7c21be0d4b51\t'
            'Wed Sep 14 14:32:35 2016 -0700\t'
            'Devin Jeanpierre\t'
            'jeanpierreda@gmail.com\t'
            'Google\'s python frame change isn\'t years old (#103)\n'

            '2d6a2cb6b696e48d4804f6a0377e07d908589cda\t'
            'Thu Sep 15 01:23:12 2016 +0400\t'
            'Oleg Broytman\t'
            'phd@phdru.name\t'
            'SSH connection sharing  (#102)\n'

            'c7135776ba1049c8d4e4c23e211ffa0c3a42adbf\t'
            'Tue Sep 13 10:13:19 2016 -0400\t'
            'Ned Deily\t'
            'nad@python.org\t'
            'Add note to pep-0101.txt to purge directory list\n'

            '298b80b669b3b110560f52a55da7feb2f8567223\t'
            'Mon Sep 12 16:36:01 2016 -0700\t'
            'Brett Cannon\t'
            'brettcannon@users.noreply.github.com\t'
            'Mark PEP 523 as final\n',

        ans='3b87611...............................PEP 432: Update for C99 initializers (#12)\n'
            'cd22b95..........................................................Fix github URLs\n'
            'e8d0ecf............................................Skip files with syntax errors\n'
            '2a4515c......................................Change emoji used in PEP 505 (#106)\n'
            'a116d3d.........PEP 3333: Fix links to web programming topic and CGI spec (#104)\n'
            'af6fab3............................Update list of PEPs as implemented in 3.6.0b1\n'
            '00d5884......................Google\'s python frame change isn\'t years old (#103)\n'
            '2d6a2cb...........................................SSH connection sharing  (#102)\n'
            'c713577.........................Add note to pep-0101.txt to purge directory list\n'
            '298b80b....................................................Mark PEP 523 as final\n'
    ),
    Case(
        log='bced8ee1b0c5afd5f44923fe0dafd784334147f8\t'
            'Sun Sep 11 17:01:02 2016 -0700\t'
            'Guido van Rossum\t'
            'guido@python.org\t'
            'Move urls from hg to github.\n'

            'c51c01869cf07993df3df0dd487d863af9e04fca\t'
            'Sun Sep 11 18:52:19 2016 +0200\t'
            'Ivan Levkivskyi\t'
            'levkivskyi@gmail.com\t'
            'Mention that private variable annotations are mangled (#101)\n'

            'ed31f2709a32bc0611558c47031a1d7eb82a8f73\t'
            'Fri Sep 9 13:31:48 2016 -0700\t'
            'Yury Selivanov\t'
            'yury@magic.io\t'
            'pep 525: Fix shutdown_asyncgens description\n'

            '835bcd8efae8ec7f8a29642aa94f15bf100d9748\t'
            'Fri Sep 9 10:37:35 2016 -0700\t'
            'Yury Selivanov\t'
            'yury@magic.io\t'
            'Mark PEP 530 as "final"\n'

            'af44514f7286566b312dea0aa0bbbdb5eea812db\t'
            'Fri Sep 9 09:48:58 2016 -0700\t'
            'Brett Cannon\t'
            'brettcannon@users.noreply.github.com\t'
            'Make a note into a note directive. (#100)\n'

            '4f8486bf81ee4bccc96bbc4f0aa35275d398d85a\t'
            'Thu Sep 8 22:06:34 2016 -0700\t'
            'Yury Selivanov\t'
            'yury@magic.io\t'
            'Mark PEPs 525 & 526 as Final; update PEP 494\n'

            '9bc423be2ab5c263b47aa187f1f2b2cc66a1a8fb\t'
            'Thu Sep 8 15:48:19 2016 -0700\t'
            'Brett Cannon\t'
            'brettcannon@users.noreply.github.com\t'
            'Update status list w/ b.p.o work in progress (#99)\n'

            '43fb14c7bc80759ce5e724b72f2510b8dfc578da\t'
            'Thu Sep 8 15:37:44 2016 -0700\t'
            'Guido van Rossum\t'
            'guido@python.org\t'
            'PEP 520 is also implemented (Erik took __definition_order__ out).\n'

            '209820e80a2ab95630d4ffaf3e3d1fb644e3f811\t'
            'Thu Sep 8 15:25:57 2016 -0700\t'
            'Guido van Rossum\t'
            'guido@python.org\t'
            'Add Resolution header to PEP 526\n'

            '9bae12b428257125c038f24cda565a84766f7ac5\t'
            'Thu Sep 8 15:22:33 2016 -0700\t'
            'ericsnowcurrently\t'
            'ericsnowcurrently@gmail.com\t'
            'Add a note about compact dict to PEP 520.\n'

            '23a4fbca5b9bc2c35dbf87d2bad56583dd40996f\t'
            'Thu Sep 8 15:19:27 2016 -0700\t'
            'Guido van Rossum\t'
            'guido@python.org\t'
            'PEP 468, 509 are implemented.\n'

            'c777ef8f75f7ecaf59cbbfe56119a438a9a3fe99\t'
            'Thu Sep 8 16:10:30 2016 -0500\t'
            'Ryan Hiebert\t'
            'ryan@ryanhiebert.com\t'
            'PEP 0468 typo (#98)\n'

            '1481aecea80c4ce3170397d198a94b45fcf161f4\t'
            'Thu Sep 8 13:39:10 2016 -0700\t'
            'ericsnowcurrently\t'
            'ericsnowcurrently@gmail.com\t'
            'PEP 468 is accepted.\n'

            '9cf9ffb58722c6cbed6d2ed297fb173795798773\t'
            'Thu Sep 8 13:16:46 2016 -0700\t'
            'ericsnowcurrently\t'
            'ericsnowcurrently@gmail.com\t'
            'Adjust PEP 468 relative to the new compact dict.\n'

            'fd5c057e268dce0c88fc7fb921e61190b6c2d3bb\t'
            'Thu Sep 8 12:55:30 2016 -0700\t'
            'Victor Stinner\t'
            'vstinner@redhat.com\t'
            'PEP 509 has been approved and implemented\n'

            'e6a278e85a0994f323b6c4c794d0bc0047ee6658\t'
            'Wed Sep 7 16:25:14 2016 -0700\t'
            'Guido van Rossum\t'
            'guido@python.org\t'
            'Accept PEP 509.\n'

            '722ccda54ac13f73839fde4b03511df5f8978cdf\t'
            'Wed Sep 7 16:22:00 2016 -0700\t'
            'Benjamin Peterson\t'
            'benjamin@python.org\t'
            'we need fixed width integer types\n'

            '437903fa0f4c8565ded198cb5a41c2791984f54f\t'
            'Wed Sep 7 14:49:47 2016 -0700\t'
            'Benjamin Peterson\t'
            'benjamin@python.org\t'
            'c++-style comments are kosher, too\n',

        ans='bced8ee.............................................Move urls from hg to github.\n'
            'c51c018.............Mention that private variable annotations are mangled (#101)\n'
            'ed31f27..............................pep 525: Fix shutdown_asyncgens description\n'
            '835bcd8..................................................Mark PEP 530 as "final"\n'
            'af44514................................Make a note into a note directive. (#100)\n'
            '4f8486b.............................Mark PEPs 525 & 526 as Final; update PEP 494\n'
            '9bc423b.......................Update status list w/ b.p.o work in progress (#99)\n'
            '43fb14c........PEP 520 is also implemented (Erik took __definition_order__ out).\n'
            '209820e.........................................Add Resolution header to PEP 526\n'
            '9bae12b................................Add a note about compact dict to PEP 520.\n'
            '23a4fbc............................................PEP 468, 509 are implemented.\n'
            'c777ef8......................................................PEP 0468 typo (#98)\n'
            '1481aec.....................................................PEP 468 is accepted.\n'
            '9cf9ffb.........................Adjust PEP 468 relative to the new compact dict.\n'
            'fd5c057................................PEP 509 has been approved and implemented\n'
            'e6a278e..........................................................Accept PEP 509.\n'
            '722ccda........................................we need fixed width integer types\n'
            '437903f.......................................c++-style comments are kosher, too\n'
    ),
]


@pytest.mark.parametrize('t', TEST_CASES)
def test_git_log(t: Case) -> None:
    inp = io.StringIO(t.log)
    out = io.StringIO()
    reformat_git_log(inp, out)
    assert out.getvalue() == t.ans
