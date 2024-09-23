import { useState } from "react";
import { FaFaceGrinBeam, FaFaceMeh, FaFaceFrown } from "react-icons/fa6";

const SentimentAnalysis = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeSentiment = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: "An error occurred while analyzing the sentiment." });
    }
    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">
        Sentiment Analysis
      </h2>
      <div className="mb-4">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze"
          className="w-full h-96 px-3 py-2 text-gray-700 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />
      </div>
      <button
        onClick={analyzeSentiment}
        disabled={loading}
        className={`w-full py-2 px-4 rounded-md text-white font-semibold ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-orange-500 hover:bg-orange-700 duration-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-opacity-50"
        }`}
      >
        {loading ? "Analyzing..." : "Analyze Sentiment"}
      </button>
      {result && (
        <div className="mt-6 p-4 bg-[#1A1A1A] rounded-md">
          <h3 className="text-lg font-semibold mb-2 text-gray-200">Results:</h3>
          {result.error ? (
            <p className="text-red-500">{result.error}</p>
          ) : (
            <ul className="space-y-1 text-white">
              <li className="flex items-center gap-2">
                <FaFaceGrinBeam color="lime" />
                Positive: {(result.positive * 100).toFixed(2)}%
              </li>
              <li className="flex items-center gap-2">
                <FaFaceMeh color="yellow" />
                Neutral: {(result.neutral * 100).toFixed(2)}%
              </li>
              <li className="flex items-center gap-2">
                <FaFaceFrown color="red" />
                Negative: {(result.negative * 100).toFixed(2)}%
              </li>
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default SentimentAnalysis;
