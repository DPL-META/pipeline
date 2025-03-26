import { Router } from "express";
import { addressControllerFactory } from "../factories/address";

const router = Router();
const controller = addressControllerFactory();

router.post("/", controller.createAddress.bind(controller));

router.delete("/:id", controller.deleteAdrees.bind(controller));

export default router;