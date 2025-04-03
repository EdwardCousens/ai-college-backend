const express = require("express");
const OpenAI = require("openai");
const bodyParser = require("body-parser");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(bodyParser.json());

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

app.post("/api/quiz", async (req, res) => {
    try {
        const quizResponses = req.body;
        const prompt = `Based on these quiz answers: ${JSON.stringify(quizResponses)}, suggest 5 universities that match these preferences.`;

        const response = await openai.chat.completions.create({
            model: "gpt-4",
            messages: [
                { role: "system", content: "You are a helpful college advisor." },
                { role: "user", content: prompt },
            ],
        });

        const recommendations = response.choices[0].message.content;
        res.json({ colleges: recommendations });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({ error: "Error processing request" });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
