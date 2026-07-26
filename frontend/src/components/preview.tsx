import { Flex } from "antd";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

function Preview({ markdown }: { markdown: string | null }) {
    return markdown!.trim() !== "" ? (
        <Markdown remarkPlugins={[remarkGfm]}>
            {markdown}
        </Markdown>
    ) : (
        <Flex justify="center" align="center" style={{ height: "100%", color: `${markdown!.trim() !== "" ? "black" : "gray"}` }}>
            <h1>No Markdown</h1>
        </Flex>
    )

};

export default Preview;