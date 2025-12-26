import mongoose from "mongoose";

const historySchema = new mongoose.Schema({
  date: String,
  status: String,
  confidence: String,
});

const userSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    image: { type: String,require:true },
    history: [historySchema],
  },
  { timestamps: true }
);

const User = mongoose.model("User", userSchema);
export default User;
