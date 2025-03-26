import { type Express } from "express";
import address from "./address";
import user from "./user";

export function configRoutes(app: Express) {
    app.get("/health", (req, res) => {
        return res.status(200).json({ message: "OK" });
    });

    app.use("/users", user);
    app.use("/addresses", address);
}
