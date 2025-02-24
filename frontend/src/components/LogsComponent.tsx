import React, { useEffect, useState } from 'react';

const LogsComponent: React.FC = () => {
    const [logs, setLogs] = useState<string[]>([]);

    useEffect(() => {
        const ws = new WebSocket(`${window.location.origin}/ws/logs`);

        ws.onopen = () => {
            console.log("WebSocket connection - ok");
        };

        ws.onmessage = (event) => {
            setLogs(prevLogs => [...prevLogs, event.data]);
        };

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        ws.onclose = (event) => {
            console.log("WebSocket closed", event);
        };

        return () => {
            ws.close();
        };
    }, []);

    return (
        <div>
            <h2>Logs:</h2>
            <pre>{logs.join('\n')}</pre>
        </div>
    );
};

export default LogsComponent;
