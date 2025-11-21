from jaxn import StreamingJSONParser, JSONParserHandler

class SearchResultArticleHandler(JSONParserHandler):
    def on_field_start(self, path: str, field_name: str):
        if field_name == "references":
            level = path.count("/") + 2
            print(f"\n{'#' * level} References\n")

    def on_field_end(self, path, field_name, value, parsed_value=None):
        if field_name == "title" and path == "":
            print(f"# {value}")

        elif field_name == "heading":
            print(f"\n\n## {value}\n")
        elif field_name == "content":
            print("\n") 

    def on_value_chunk(self, path, field_name, chunk):
        if field_name == "content":
            print(chunk, end="", flush=True)

    def on_array_item_end(self, path, field_name, item=None):
        if field_name == "references":
            title = item.get("title", "")
            filename = item.get("filename", "")
            print(f"- [{title}]({filename})")
