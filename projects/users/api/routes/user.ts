import { Router } from "express";
import { userControllerFactory } from "../factories/user";

const router = Router()
const controller = userControllerFactory();

router.get("/", controller.listUser.bind(controller));

router.post("/", controller.createUser.bind(controller));

router.patch("/:id", controller.updateUser.bind(controller));

router.delete("/:id", controller.deleteUser.bind(controller));

export default router;