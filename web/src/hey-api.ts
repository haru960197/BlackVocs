import type { CreateClientConfig } from './lib/api/client.gen';

export const createClientConfig: CreateClientConfig = (config) => ({
  ...config,
  baseUrl: 'http://localhost:4000',
});
