import { ChatGroq } from "@langchain/groq";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";

const model = new ChatGroq({
    apiKey: process.env.GROQ_API_KEY,
});

const sysmessage = new SystemMessage("You're Agent 47")
const message = new HumanMessage("who are you?");

const res = await model.invoke([message, sysmessage]);

console.log(res)