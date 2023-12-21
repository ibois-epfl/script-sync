import type { BaseEnvironment } from '../environment/environment.js';
import type { GeneratorFeatures } from './generator-features.js';
import type { GeneratorOptions } from './generator-options.js';

export type EnvironmentGenerator = {
  readonly env: BaseEnvironment;
  readonly features: unknown;

  emit(eventName: string | symbol, ...args: any[]): boolean;
  on(eventName: string | symbol, listener: (...args: any[]) => void): unknown;
  once(eventName: string | symbol, listener: (...args: any[]) => void): unknown;

  _postConstruct?(): Promise<void>;

  /**
   * Get the generator destination root directory.
   */
  destinationRoot(): string;
  /**
   * Set the generator destination root directory.
   */
  // eslint-disable-next-line @typescript-eslint/unified-signatures
  destinationRoot(rootPath: string): string;

  // Generator >= v5
  queueTasks?(): Promise<void>;
};

export type BaseGenerator<
  O extends GeneratorOptions = GeneratorOptions,
  F extends GeneratorFeatures = GeneratorFeatures,
> = EnvironmentGenerator & {
  readonly options: O;

  // Generator >= v5
  readonly features: F | undefined;
};

export type BaseGeneratorConstructor<
  O extends GeneratorOptions = GeneratorOptions,
  F extends GeneratorFeatures = GeneratorFeatures,
> = (new (args?: string[], options?: O, features?: F) => BaseGenerator<O, F>) & (new (options?: O, features?: F) => BaseGenerator<O, F>);
