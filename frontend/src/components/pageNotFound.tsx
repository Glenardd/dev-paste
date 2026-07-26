import { Button, Flex, Result } from 'antd';
import { useNavigate } from 'react-router-dom';

export default function PageNotFound() {

    const navigate = useNavigate();

    return (
        <>
            <Flex justify='center' align='center' style={{ width: "100%", height: "100vh" }}>
                <Result
                    status="404"
                    title="404"
                    subTitle="Sorry, the page you visited does not exist."
                    extra={<Button type="primary" onClick={() => navigate("/")}>Return to editor</Button>}
                />
            </Flex>
        </>
    );
};
