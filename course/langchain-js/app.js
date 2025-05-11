import 'dotenv/config';
import { ChatGroq } from "@langchain/groq";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";

const model = new ChatGroq({
    model: "mixtral-8x7b-32768",
    temperature: 0,
    apiKey: process.env.GROQ_API_KEY
});

const messages = [
    new SystemMessage("Translate the following from English into Italian"),
    new HumanMessage("hi!"),
];

(async () => {
    console.log(await model.invoke(messages));
    console.log(await model.invoke("Hello"));
    console.log(await model.invoke([{ role: "user", content: "Hello" }]));
    console.log(await model.invoke([new HumanMessage("hi!")]));
})();
