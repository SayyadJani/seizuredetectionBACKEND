import dotenv from "dotenv";
dotenv.config();

import express from "express";
import cors from "cors";
import userRoutes from "./routes/userRoutes.js";
import authRoutes from "./routes/authRoutes.js";
import connectDB from "./config/db.js";

const app = express();

// Connect DB
connectDB();

// Middleware
app.use(
  cors({
    origin: "*", // TEMPORARY (works for dev & prod)
    credentials: true,
  })
);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Test route
app.get("/", (req, res) => {
  res.json({ message: "Backend is running successfully" });
});

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/user", userRoutes);

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
