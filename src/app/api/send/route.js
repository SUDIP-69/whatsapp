import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(request) {
  const { phone, message } = await request.json();

  // Validate input
  if (!phone?.startsWith('+') || !message?.trim()) {
    return NextResponse.json(
      { success: false, error: 'Invalid phone or message format' },
      { status: 400 }
    );
  }

  try {
    const result = await new Promise((resolve, reject) => {
      const scriptPath = path.join(process.cwd(), 'scripts/send_whatsapp.py');
      const pythonProcess = spawn('python', [scriptPath, phone, message]);

      let output = '';
      let errorOutput = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code !== 0 || errorOutput) {
          reject(`Python Error [${code}]: ${errorOutput || output}`);
        } else {
          resolve(output);
        }
      });
    });

    return NextResponse.json({ success: true, result });
  } catch (error) {
    console.error('Server Error:', error);
    return NextResponse.json(
      { success: false, error: error.message || error },
      { status: 500 }
    );
  }
}