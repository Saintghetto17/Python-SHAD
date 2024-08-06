from testlib.docs import is_function_docstring_exists, is_class_docstring_exists


class TestFunctionDocs:
    def test_no_doc(self) -> None:
        def _foo() -> None:
            return

        assert not is_function_docstring_exists(_foo)

    def test_empty_doc(self) -> None:
        def _foo() -> None:
            """"""
            return

        assert not is_function_docstring_exists(_foo)

    def test_empty_doc_with_split(self) -> None:
        def _foo() -> None:
            """
            """
            return

        assert not is_function_docstring_exists(_foo)

    def test_one_line_doc(self) -> None:
        def _foo() -> None:
            """Some line as a docstring"""
            return

        assert is_function_docstring_exists(_foo)

    def test_multi_line_doc(self) -> None:
        def _foo() -> None:
            """Some line as a docstring
            More and more lines
            """
            return

        assert is_function_docstring_exists(_foo)

    def test_missing_param_doc(self) -> None:
        def _foo(a: int) -> int:
            """
            Some docstring
            :return: Some return
            """
            return 0

        assert is_function_docstring_exists(_foo)

    def test_missing_return_doc(self) -> None:
        def _foo(a: int) -> int:
            """
            Some docstring
            :param a: Some param
            """
            return 0

        assert is_function_docstring_exists(_foo)

    def test_full_doc(self) -> None:
        def _foo(a: int) -> int:
            """
            Some docstring
            :param a: Some param
            :return: Some return
            """
            return 0

        assert is_function_docstring_exists(_foo)


class TestClassDocs:
    def test_no_doc(self) -> None:
        class A:
            pass

        assert not is_class_docstring_exists(A)

    def test_empty_doc(self) -> None:
        class A:
            """"""
            pass

        assert not is_class_docstring_exists(A)

    def test_empty_doc_with_split(self) -> None:
        class A:
            """
            """
            pass

        assert not is_class_docstring_exists(A)

    def test_one_line_doc(self) -> None:
        class A:
            """Some docstring"""
            pass

        assert is_class_docstring_exists(A)

    def test_multi_line_doc(self) -> None:
        class A:
            """Some line as a docstring
            More and more lines
            """
            pass

        assert is_class_docstring_exists(A)


class TestModuleDocs:
    pass
