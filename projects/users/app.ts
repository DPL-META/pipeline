import 'dotenv/config';
import express from "express";
import { configRoutes } from "./api/routes/index";
const app = express();

app.use(express.json());

configRoutes(app);
app.listen(process.env.PORT, () => {
    console.log(`Server listening on ${process.env.PORT}`);
});