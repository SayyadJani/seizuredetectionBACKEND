import cloudinary from "cloudinary";

const cloudinaryV2 = cloudinary.v2;

cloudinaryV2.config({
  cloud_name: process.env.CLOUD_NAME,
  api_key: process.env.CLOUD_API_KEY,
  api_secret: process.env.CLOUD_API_SECRET,
});

export async function uploadImage(filePath) {
  const result = await cloudinaryV2.uploader.upload(filePath, {
    folder: "users",
  });
  return result.secure_url;
}
console.log("Cloudinary:", {
  name: process.env.CLOUD_NAME,
  key: process.env.CLOUD_API_KEY,
});
