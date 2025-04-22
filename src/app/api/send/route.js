import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(request) {
  const { phone, message } = await request.json();
  
  try {
    // Validate input
    if (!phone || !message) {
      throw new Error('Phone number and message are required');
    }

    // Get script path
    let scriptPath = path.join(process.cwd(),'src', 'scripts', 'send_whatsapp.py');
    
    // Windows path fix
    if (process.platform === 'win64') {
      scriptPath = scriptPath.replace(/\\/g, '/');
    }

    // Verify file exists
    const fs = await import('fs');
    if (!fs.existsSync(scriptPath)) {
      throw new Error(`Python script not found at ${scriptPath}`);
    }

    const result = await new Promise((resolve, reject) => {
      const pythonProcess = spawn('python', [scriptPath, phone, message], {
        shell: process.platform === 'win32'
      });

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
          reject(errorOutput || `Process exited with code ${code}`);
        } else {
          resolve(output);
        }
      });
    });

    return NextResponse.json({ 
      success: true, 
      result: result.trim() 
    });

  } catch (error) {
    console.error('Server Error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: error.message || 'Failed to send message',
        details: process.env.NODE_ENV === 'development' ? error.stack : undefined
      },
      { status: 500 }
    );
  }
}