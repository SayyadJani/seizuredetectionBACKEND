import User from "../models/user.js";

// ADD SEIZURE HISTORY
export const addHistory = async (req, res) => {
  try {
    const { status, confidence } = req.body;

    const user = await User.findById(req.user._id);
    if (!user)
      return res.status(404).json({ message: "User not found" });

    user.history.push({
      date: new Date().toISOString().split("T")[0],
      status,
      confidence,
    });

    await user.save();

    res.json({
      message: "History added successfully",
      history: user.history,
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET HISTORY
export const getHistory = async (req, res) => {
  try {
    res.json(req.user.history);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
