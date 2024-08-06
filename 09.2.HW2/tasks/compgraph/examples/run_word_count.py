import click

from compgraph.algorithms import word_count_graph


# TODO: cli
# You can use anything you want. We suggest you to use `click`
def main() -> None:
    graph = word_count_graph(input_stream_name="input", text_column='text', count_column='count')

    input_filepath = None
    output_filepath = None

    result = graph.run(input=lambda: input_filepath)
    with open(output_filepath, "w") as out:
        for row in result:
            print(row, file=out)


if __name__ == "__main__":
    main()
