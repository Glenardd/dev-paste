import { Flex } from "antd";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "github-markdown-css/github-markdown-light.css";
import "highlight.js/styles/github.css";

function Preview({ markdown }: { markdown: string | null }) {
  const content = markdown ?? "";

  if (content.trim() === "") {
    return (
      <Flex justify="center" align="center" style={{ height: "100%", color: "gray" }}>
        <h1>No Markdown</h1>
      </Flex>
    );
  }

  return (
    <div className="markdown-body">
      <Markdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
        {content}
      </Markdown>
    </div>
  );
}

export default Preview;