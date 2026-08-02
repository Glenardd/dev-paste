import { useEffect, useState } from "react";
import TextEditor from "./components/TextEditor";
import Preview from "./components/preview";
import { Button } from "antd";
import { notification } from 'antd';
import { Link, useParams } from "react-router";
import { useNavigate } from "react-router";
import axios from "axios";
import { api } from "./api/api";
import { GithubFilled } from '@ant-design/icons';

function App() {

  const [markDown, setMarkDown] = useState("");
  const [snippetContent, setSnippeContent] = useState("");
  const get_markdown = (value: string) => setMarkDown(value);
  const [notification_api, notification_context] = notification.useNotification();

  let navigate = useNavigate();
  let { id } = useParams<{ id: string }>();

  const shareLink = async () => {
    try {
      const payload = {
        content: `${markDown}`
      };

      const response = await api.post("api/v1/snippets", payload);
      const generatedId = response.data.id;

      // copies the id of the 
      console.log(generatedId);
      await navigator.clipboard.writeText(generatedId);

    } catch (error) {
      if (axios.isAxiosError(error)) {
        // rate limit error
        if (error.response?.status === 429) {
          notification_api.error({
            title: "Rate limit reached",
            description: "Too many request, please wait",
            duration: 2,
            showProgress: true
          });

          return;
        };

        // service not available
        if (error.response?.status === 404) {
          notification_api.error({
            title: "Service unavailable",
            description: "The application couldn't reach the requested service.",
            duration: 2,
            showProgress: true
          });

          return;
        }

        //checks if api is offline
        if (error.code === "ERR_NETWORK") {
          console.log("API is offline or unreachable");
          notification_api.error({
            title: "API is offline or unreachable",
            description: "come back again",
            duration: 2,
            showProgress: true
          });

          return;
        };
      }
    };

    // if markdown is undefined
    if (!markDown.trim()) {
      notification_api.error({
        title: "Error Sharing",
        description: "Don't leave empty",
        duration: 2,
        showProgress: true
      });

      return;
    };

    notification_api.success({
      title: "Link Copied",
      description: "Ready for sharing",
      duration: 2,
      showProgress: true
    });
  };

  // download markdown to txt
  const download = () => {
    const content = id ? snippetContent : markDown;

    if (!content.trim()) {
      notification_api.error({
        title: "No markdown found",
        description: "please atleast input a markdown",
        duration: 2,
        showProgress: true
      });

      return;
    };

    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "note.txt"

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  useEffect(() => {
    if (!id) return;

    const fetchMarkUp = async () => {

      try {
        const response = await api.get(`/api/v1/snippets/${id}`);
        setSnippeContent(response.data!.content)
      } catch (error) {
        if (axios.isAxiosError(error)) {
          if (error.response?.status === 404) {
            notification_api.error({
              title: "No markdown found",
              description: "invalid markdown",
              duration: 2,
              showProgress: true
            });
          };

          if (error.code === "ERR_NETWORK") {
            notification_api.error({
              title: "API is offline or unreachable",
              description: "come back again",
              duration: 2,
              showProgress: true
            });
          };

          // rate limit error
          if (error.response?.status === 429) {
            notification_api.error({
              title: "Rate limit reached",
              description: "Too many request, please wait",
              duration: 2,
              showProgress: true
            });
          };
        };
      };
    };

    // updates the markdon content in db
    const updateMarkdown = async () => {
      try {
        const response = await api.get('api/v1/snippets/all');
        if(response.status ===200){
          console.log("markdown updated successfully");
        };

      } catch (error) {
        return;
      }
    }

    updateMarkdown();
    fetchMarkUp();
  }, [id]);

  return (
    <div className="wrapper">
      {notification_context}
      {id && (<div>
        <Button type="primary" size={"large"} onClick={() => { navigate('/') }}>Return</Button>
      </div>)}
      <div className={`container container-split ${id ? "container-preview-only" : ""}`}>
        {
          !id && (
            <div className="panel panel-editor">
              <TextEditor markdown={get_markdown} />
            </div>
          )
        }
        <div className="panel panel-preview">
          {id ? (<Preview markdown={snippetContent} />) : (<Preview markdown={markDown} />)}
        </div>
      </div>
      <div className="buttons buttons-in-between">
        <div className="buttons">
          <Button type="primary" size={"large"} onClick={() => shareLink()}>Share</Button>
          <Button type="primary" size={"large"} onClick={() => download()} >Download</Button>
        </div>
        <div className="buttons">
          <Link to="https://github.com/Glenardd/dev-paste">
            <GithubFilled style={{ color: "#1677ff", fontSize: '32px' }} />
          </Link>
        </div>
      </div>
    </div>
  );
}

export default App;