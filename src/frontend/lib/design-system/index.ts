/**
 * Public design-system surface. Pages and feature code import from here.
 *
 * Boundary rule (enforced by .claude/lib/handlers/import_boundaries.py):
 *   - Routes & feature code may import from this barrel and from `./primitives`,
 *     `./composed`. They MAY NOT import from `./internal/`.
 */

export { cn } from './cn.js';
export { cva, type CvaConfig, type CvaProps } from './cva.js';
export {
  colorTokens,
  radiusTokens,
  shadowTokens,
  typeScaleTokens,
  motionTokens,
  STATUS_KEYS,
  SIZE_KEYS,
  type StatusKey,
  type SizeKey,
} from './tokens.js';
export {
  statusToPalette,
  healthBandToStatus,
  healthBandLabel,
  trendToStatus,
  trendGlyph,
  sectToStatus,
  sectLabel,
  canonicalTierToStatus,
  canonicalTierLabel,
  ingestPhaseToStatus,
  type HealthBand,
  type TrendDirection,
  type Sect,
  type CanonicalTier,
  type IngestPhaseStatus,
} from './variants.js';
export type { BaseProps, ElementProps, VariantProps } from './contracts.js';

export * from './primitives/index.js';
export * from './composed/index.js';
