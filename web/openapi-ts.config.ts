import { defineConfig } from '@hey-api/openapi-ts';
import * as dotenv from 'dotenv';

dotenv.config();

export default defineConfig({
  input: `${process.env.SERVICE_URI}/openapi.json`,
  output: 'src/lib/api/',
  plugins: [{
    name: '@hey-api/client-next',
    runtimeConfigPath: './src/hey-api.ts',
  }],
});
