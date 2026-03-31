import express from "express";
import authMiddleware from "../middleware/authMiddleware.js";
import upload from "../middleware/uploadMiddleware.js";
import { addHistory,getHistory } from "../controllers/userController.js";
import { predictSeizure } from "../controllers/predictionController.js";
const router = express.Router();

router.get("/profile", authMiddleware, (req, res) => {
  res.json(req.user);
});

router.post("/history", authMiddleware, addHistory);

router.get("/history", authMiddleware, getHistory);

router.post("/predict", authMiddleware, upload.single("eegFile"), predictSeizure);

export default router;
