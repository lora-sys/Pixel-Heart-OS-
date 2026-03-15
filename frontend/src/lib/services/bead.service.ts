/**
 * Bead Service - API client for beads endpoints
 */
import { dedupedFetch } from '../api/client';
import type { Bead } from '../types/shared-types';

export interface BeadCreate {
  parent_id?: string;
  branch_name: string;
  action: string;
  emotion_tag?: string;
  content: Record<string, any>;
  signature?: string;
}

export interface BeadResponse extends Bead {
  timestamp: string;
}

export interface BranchCreate {
  branch_name: string;
  from_bead_id: string;
}

export interface BranchResponse {
  branch_name: string;
  head_bead_id: string;
  message: string;
}

export interface BeadDiffChange {
  field: string;
  from: any;
  to: any;
}

export interface BeadDiffResponse {
  bead_id_earlier: string;
  bead_id_later: string;
  changes: BeadDiffChange[];
}

class BeadService {
  private basePath = '/api/v1/beads';

  async getTimeline(
    branch?: string,
    limit: number = 100,
    offset: number = 0
  ): Promise<BeadResponse[]> {
    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
      ...(branch && { branch })
    });
    return dedupedFetch<BeadResponse[]>(`${this.basePath}/timeline?${params}`, {
      cacheKey: `beads:timeline:${branch || 'main'}:${limit}:${offset}`,
      cacheTtl: 60000 // 1 minute
    });
  }

  async create(data: BeadCreate): Promise<BeadResponse> {
    return dedupedFetch<BeadResponse>(this.basePath, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async createBranch(branchName: string, fromBeadId: string): Promise<BranchResponse> {
    return dedupedFetch<BranchResponse>(`${this.basePath}/branch`, {
      method: 'POST',
      body: JSON.stringify({ branch_name: branchName, from_bead_id: fromBeadId })
    });
  }

  async diff(beadId1: string, beadId2: string): Promise<BeadDiffResponse> {
    return dedupedFetch<BeadDiffResponse>(`${this.basePath}/diff/${beadId1}/${beadId2}`);
  }

  async listBranches(): Promise<{ branches: Array<{ name: string; head_bead_id: string; head_timestamp: string }> }> {
    return dedupedFetch(`/${this.basePath}/branches`, {
      cacheKey: 'branches:all',
      cacheTtl: 120000 // 2 minutes
    });
  }

  async getBead(id: string): Promise<BeadResponse> {
    // Individual bead fetch not in API yet
    throw new Error('Not implemented');
  }
}

export const beadService = new BeadService();
