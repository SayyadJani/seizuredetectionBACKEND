import { spawn } from "child_process";
import path from "path";
import os from "os";
import fs from "fs";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const predictSeizure = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const filePath = req.file.path;
    const pythonScript = path.join(__dirname, "..", "ml", "predict.py");

    // Path to virtual environment python
    const venvPython = path.join(__dirname, "..", "venv", "Scripts", "python.exe");
    const pythonExec = fs.existsSync(venvPython) ? venvPython : "python";

    // Command to run python script
    const pythonProcess = spawn(pythonExec, [pythonScript, filePath]);

    let dataString = "";

    pythonProcess.stdout.on("data", (data) => {
      dataString += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      const errorMsg = data.toString();
      console.error(`Python stderr: ${errorMsg}`);
      dataString += `[ERROR_LOG]: ${errorMsg}`; // Append error to catch it in closed
    });

    pythonProcess.on("close", (code) => {
      // 1. Cleanup uploaded file
      try {
        if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
      } catch (err) {
        console.error("Cleanup error:", err);
      }

      if (code !== 0) {
        return res
          .status(500)
          .json({ 
            error: "Clinical Insight Failure", 
            details: dataString.includes("ModuleNotFoundError") 
              ? "Python ML dependencies (TensorFlow/Numpy) not correctly initialized on server." 
              : "Backend execution failed. Ensure Python environment is configured.",
            raw: dataString
          });
      }

      try {
        // Find JSON part only, in case there were logs
        const jsonStart = dataString.indexOf('{');
        if (jsonStart === -1) throw new Error("No JSON in output");
        
        const result = JSON.parse(dataString.substring(jsonStart));
        if (result.error) {
          return res.status(500).json({ error: result.error, details: "ML Engine internal error." });
        }
        res.json(result);
      } catch (err) {
        res.status(500).json({ error: "Failed to parse clinical diagnostics", details: "Memory limit or environment mismatch.", raw: dataString });
      }
    });
  } catch (error) {
    console.error("Error in prediction controller:", error);
    res.status(500).json({ error: "Server error during prediction" });
  }
};
