import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const CheckMolePage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const navigate = useNavigate();

  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedImage(URL.createObjectURL(e.target.files[0]));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Placeholder for submission logic
    console.log('Form submitted');
  };

  return (
    <div className="bg-gray-50 min-h-screen flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white p-8 rounded-lg shadow-md relative">
        <button
          onClick={() => navigate('/')}
          className="absolute top-4 right-4 text-gray-600 hover:text-gray-800"
        >
          <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-6">
          Please upload a picture of your mole
        </h1>

        <div className="space-y-4 text-gray-600 mb-8">
          <div>
            <h2 className="font-semibold text-lg text-gray-800">Only One Photo Per Mole</h2>
            <ul className="list-disc list-inside ml-4">
              <li>Upload one clear photo of the mole.</li>
              <li>Make sure it’s well-framed and focused.</li>
            </ul>
          </div>
          <div>
            <h2 className="font-semibold text-lg text-gray-800">Auto-Focus on the Mole</h2>
            <ul className="list-disc list-inside ml-4">
              <li>Let your smartphone auto-focus before taking the photo.</li>
              <li>Wait a second to let the camera focus specifically on the mole.</li>
            </ul>
          </div>
          <div>
            <h2 className="font-semibold text-lg text-gray-800">Don’t Get Too Close</h2>
            <ul className="list-disc list-inside ml-4">
              <li>Being too close may cause the photo to be blurry.</li>
              <li>Instead, step back slightly and use zoom to capture the mole clearly.</li>
            </ul>
          </div>
          <div>
            <h2 className="font-semibold text-lg text-gray-800">Review Your Photo Before Uploading</h2>
            <ul className="list-disc list-inside ml-4">
              <li>Ensure the mole is in focus, centered, and well-lit.</li>
              <li>Poor image quality can prevent accurate diagnosis.</li>
            </ul>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700">
              Upload Image
            </label>
            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
              <div className="space-y-1 text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <div className="flex text-sm text-gray-600">
                  <label htmlFor="file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                    <span>Upload a file</span>
                    <input id="file-upload" name="file-upload" type="file" className="sr-only" accept=".jpg,.png" onChange={handleImageChange} />
                  </label>
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs text-gray-500">
                  PNG, JPG up to 10MB
                </p>
              </div>
            </div>
          </div>

          {selectedImage && (
            <div className="mt-4">
              <h3 className="text-lg font-medium text-gray-800 mb-2">Image Preview:</h3>
              <img src={selectedImage} alt="Mole preview" className="w-full h-auto rounded-lg shadow-md" />
            </div>
          )}

          <div>
            <button type="submit" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CheckMolePage;
