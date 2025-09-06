import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const CheckMolePage = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleAnalyze = () => {
    if (file) {
      setMessage(`Analyzing ${file.name}... (This is a placeholder)`);
      // In a real app, you would send the file to the backend for analysis.
    } else {
      setMessage('Please select a file first.');
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
