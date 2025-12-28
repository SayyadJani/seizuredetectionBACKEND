import dotenv from "dotenv";
dotenv.config(); 

import express from "express";
import cors from "cors";
import userRoutes from "./routes/userRoutes.js";
import connectDB from "./config/db.js";
import authRoutes from "./routes/authRoutes.js";

const app = express();

connectDB();

app.use(
  cors({
<<<<<<< HEAD
    origin: "*", 
    credentials: true,
  })
);app.use(express.json());
=======
    origin: "*", // TEMPORARY (for debugging)
    credentials: true,
  })
);
app.use(express.json());
>>>>>>> aca2bbdf9fb025b70ce0e3e9e0c50fec4f404b56
app.use(express.urlencoded({ extended: true }));


app.get("/", (req, res) => {
  res.json({ message: "Backend is running successfully" });
});

app.use("/api/auth", authRoutes);
app.use("/api/user", userRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
