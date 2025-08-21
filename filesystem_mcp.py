from mcp.server.fastmcp import FastMCP
import os


mcp = FastMCP("EducosysFileSystem")


@mcp.tool()
def addFile(filename: str):
   """Create a new file in current directory"""
   if not os.path.exists(filename):
       with open(filename, "w") as f:
           pass
       print(f"File '{filename}' created.")
   else:
       print(f"File '{filename}' already exists.")


@mcp.tool()
def addFolder(directory_name: str):
   """Create a new Directory in current directory"""
   if not os.path.exists(directory_name):
       os.mkdir(directory_name)
       print(f"Directory '{directory_name}' created.")
   else:
       print(f"Directory '{directory_name}' already exists.")


@mcp.tool()
def writeFile(path: str, content: str, append: bool = False):
    """Write content to a file at the given path."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "a" if append else "w"
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)
    return f"Content {'appended to' if append else 'written to'} '{path}' successfully."

@mcp.tool()
def deleteFile(path: str):
    """Delete a file from current directory."""
    if os.path.exists(path):
        os.remove(path)
        return f"File '{path}' deleted successfully."
    else:
        return f"File '{path}' does not exist."






if __name__ == "__main__":
   mcp.run(transport="stdio")