import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const CheckMolePage = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleAnalyze = async () => {
    if (!file) {
      setMessage('Please select a file first.');
      return;
    }

    // Retrieve token from local storage
    const tokenData = JSON.parse(localStorage.getItem('authToken'));
    if (!tokenData || !tokenData.access_token) {
        setMessage('You must be logged in to analyze a mole.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setMessage('Analyzing...');
    setAnalysisResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${tokenData.access_token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const result = await response.json();
      setAnalysisResult(result);
      setMessage('Analysis complete.');
    } catch (error) {
      console.error('Analysis error:', error);
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <CardTitle>Check a Mole</CardTitle>
          <CardDescription>Upload a picture of a mole for analysis.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-4 text-sm text-gray-700">
            <h3 className="font-semibold text-base text-gray-900">Instructions for Uploading Mole Photos</h3>
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold">Only One Photo Per Mole</h4>
                <ul className="list-disc pl-5 space-y-1">
                  <li>Upload one clear photo of the mole.</li>
                  <li>Make sure it’s well-framed and focused.</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold">Auto-Focus on the Mole</h4>
                <ul className="list-disc pl-5 space-y-1">
                  <li>Let your smartphone auto-focus before taking the photo.</li>
                  <li>Wait a second to let the camera focus specifically on the mole.</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold">Don’t Get Too Close</h4>
                <ul className="list-disc pl-5 space-y-1">
                  <li>Being too close may cause the photo to be blurry.</li>
                  <li>Instead, step back slightly and use zoom to capture the mole clearly.</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold">Review Your Photo Before Uploading</h4>
                <ul className="list-disc pl-5 space-y-1">
                  <li>Ensure the mole is in focus, centered, and well-lit.</li>
                  <li>Poor image quality can prevent accurate diagnosis.</li>
                </ul>
              </div>
            </div>
          </div>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="mole-picture">Mole Picture</Label>
              <Input id="mole-picture" type="file" onChange={handleFileChange} />
            </div>
            {message && <p className="text-sm text-gray-600 mt-4">{message}</p>}
            {analysisResult && (
              <div className="mt-4 space-y-4">
                <div className="p-4 bg-gray-50 rounded-md">
                  <h4 className="font-semibold text-gray-800">Analysis Result</h4>
                  <p className="text-sm text-gray-600">
                      Probability of Melanoma: {analysisResult.cnn_result.toFixed(4)}
                  </p>
                </div>
                
                {analysisResult.similar_images && analysisResult.similar_images.length > 0 ? (
                  <div className="p-4 bg-blue-50 rounded-md">
                    <h4 className="font-semibold text-gray-800 mb-3">Similar Mole Images</h4>
                    <p className="text-sm text-gray-600 mb-4">
                      Here are the {analysisResult.similar_images.length} most similar moles from our medical database:
                    </p>
                    <div className="grid grid-cols-3 gap-3">
                      {analysisResult.similar_images.map((similarImage, index) => (
                        <div key={similarImage.image_id} className="relative group">
                          <img
                            src={similarImage.image_url}
                            alt={similarImage.image_id}
                            className="w-full h-20 object-cover rounded-md border"
                            onError={(e) => {
                              e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0zNS41IDM1LjVMMzUuNSA2NC41IiBzdHJva2U9IiM2QjcyODAiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik02NC41IDM1LjVMNjQuNSA2NC41IiBzdHJva2U9IiM2QjcyODAiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjwvZz4KPC9zdmc+Cg==';
                            }}
                          />
                          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-70 transition-opacity duration-200 rounded-md flex items-center justify-center">
                            <div className="opacity-0 group-hover:opacity-100 text-white text-xs text-center p-2 transition-opacity duration-200">
                              <div className="font-semibold text-xs mb-1">{similarImage.image_id}</div>
                              <div className="font-semibold">{similarImage.diagnosis.toUpperCase()}</div>
                              <div>{similarImage.age ? `${similarImage.age}y` : 'Age: N/A'}</div>
                              <div>{similarImage.sex}</div>
                              <div>{similarImage.localization}</div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="mt-3 text-xs text-gray-500">
                      <p><strong>Legend:</strong> Hover over images to see details. These are similar cases from medical literature to help provide context.</p>
                      <p className="mt-1"><strong>Note:</strong> This tool is for educational purposes only and should not replace professional medical advice.</p>
                    </div>
                  </div>
                ) : (
                  <div className="p-4 bg-yellow-50 rounded-md">
                    <h4 className="font-semibold text-gray-800 mb-2">Similar Images</h4>
                    <p className="text-sm text-gray-600">
                      Similar image comparison is temporarily unavailable. Your mole analysis result above is still accurate.
                    </p>
                    <p className="text-xs text-gray-500 mt-2">
                      <strong>Note:</strong> The similarity feature requires database preparation and will be available soon.
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </CardContent>
        <CardFooter>
          <Button onClick={handleAnalyze} className="w-full">
            Analyze
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default CheckMolePage;
