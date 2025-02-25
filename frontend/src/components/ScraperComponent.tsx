import * as React from "react";
import axios from "axios";


export const ScraperComponent: React.FC = () => {
    const [message, setMessage] = React.useState<string>("");
    const [loading, setLoading] = React.useState<boolean>(false);
    const [error, setError] = React.useState<string>("");

    const handleScraping = async () => {
        setLoading(true);
        setMessage("");
        setError("");

        try {
            const response = await axios.post("http://localhost:8000/api/v1/scrap-ingredients");
            setMessage(response.data.message);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <h2>Run scraping</h2>
            <br/>
            <button onClick={handleScraping}>
                {loading ? "Loading..." : "Run scraping"}
            </button>
            {message && <p>{message}</p>}
            {error && <p style={{color: "red"}}>{error}</p>}
        </>
    );
};

export default ScraperComponent;