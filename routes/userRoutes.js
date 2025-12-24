import express from "express";
import authMiddleware from "../middleware/authMiddleware.js";
import { addHistory,getHistory } from "../controllers/userController.js";
const router = express.Router();

router.get("/profile", authMiddleware, (req, res) => {
  res.json(req.user);
});

router.post("/history", authMiddleware, addHistory);

router.get("/history", authMiddleware, getHistory);

export default router;
