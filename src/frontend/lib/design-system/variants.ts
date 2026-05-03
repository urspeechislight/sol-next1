/**
 * Variant-map registry. Single source of truth for "what color/badge/icon
 * represents this status across the entire app."
 *
 * Pages and feature code reference these maps — never literal classes — so
 * rebranding or theme tweaks happen in one place.
 *
 * Rule (enforced by .claude/lib/handlers/variant_consistency.py):
 *   - Every domain-status enum (e.g. health bands, account stages) must be
 *     declared here, not inline in components.
 */

import type { StatusKey } from './tokens.js';

/* ---- Generic status → palette ---------------------------------------------- */

export const statusToPalette: Record<
  StatusKey,
  { fg: string; bg: string; soft: string; border: string }
> = {
  accent: {
    fg: 'text-accent',
    bg: 'bg-accent',
    soft: 'bg-accent-soft',
    border: 'border-accent',
  },
  success: {
    fg: 'text-success',
    bg: 'bg-success',
    soft: 'bg-success-soft',
    border: 'border-success',
  },
  warning: {
    fg: 'text-warning',
    bg: 'bg-warning',
    soft: 'bg-warning-soft',
    border: 'border-warning',
  },
  danger: {
    fg: 'text-danger',
    bg: 'bg-danger',
    soft: 'bg-danger-soft',
    border: 'border-danger',
  },
  info: { fg: 'text-info', bg: 'bg-info', soft: 'bg-info-soft', border: 'border-info' },
  muted: {
    fg: 'text-muted',
    bg: 'bg-muted',
    soft: 'bg-muted-soft',
    border: 'border-muted',
  },
};

/* ---- Health band → status (example domain map) ------------------------------ */

export type HealthBand = 'strong' | 'stable' | 'at_risk' | 'critical' | 'unknown';

export const healthBandToStatus: Record<HealthBand, StatusKey> = {
  strong: 'success',
  stable: 'accent',
  at_risk: 'warning',
  critical: 'danger',
  unknown: 'muted',
};

export const healthBandLabel: Record<HealthBand, string> = {
  strong: 'Strong',
  stable: 'Stable',
  at_risk: 'At risk',
  critical: 'Critical',
  unknown: 'Unknown',
};

/* ---- Trend direction → status ----------------------------------------------- */

export type TrendDirection = 'up' | 'down' | 'flat';

export const trendToStatus: Record<TrendDirection, StatusKey> = {
  up: 'success',
  down: 'danger',
  flat: 'muted',
};

export const trendGlyph: Record<TrendDirection, string> = {
  up: '▲',
  down: '▼',
  flat: '▬',
};
