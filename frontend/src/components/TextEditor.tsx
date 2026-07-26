import { Input } from 'antd';

function TextEditor(
    { markdown }:
        { markdown: (value: string) => void }
) {

    return (
        <>
            {/* <h2>TextEditor</h2> */}
            <Input.TextArea
                id="editor" 
                onChange={(e) => markdown(e.target.value)}
                name="editor"
                autoFocus
                placeholder="Start typing..."
                style={{
                    width: "100%",
                    height: "100%",
                    resize: "none",
                }}
            >
            </Input.TextArea>
        </>
    );
};

export default TextEditor;