import dotenv from "dotenv";
dotenv.config(); // ✅ FORCE LOAD ENV HERE

import cloudinary from "cloudinary";

const cloudinaryV2 = cloudinary.v2;

cloudinaryV2.config({
  cloud_name: process.env.CLOUD_NAME,
  api_key: process.env.CLOUD_API_KEY,
  api_secret: process.env.CLOUD_API_SECRET,
});

export function uploadImageFromBuffer(fileBuffer) {
  return new Promise((resolve, reject) => {
    cloudinaryV2.uploader.upload_stream(
      { folder: "users" },
      (error, result) => {
        if (error) reject(error);
        else resolve(result.secure_url);
      }
    ).end(fileBuffer);
  });
}
