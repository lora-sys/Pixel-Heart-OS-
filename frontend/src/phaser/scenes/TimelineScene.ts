import { Scene } from 'phaser';

interface BeadData {
  id: string;
  action: string;
  timestamp: string;
  emotion_tag?: string;
}

export class TimelineScene extends Scene {
  private beads: BeadData[] = [];
  private beadGraphics: Map<string, any> = new Map();
  private selectedIndex: string | null = null;
  private scrollOffset: number = 0;

  constructor() {
    super({ key: 'TimelineScene' });
  }

  create() {
    const width = this.scale.width;
    const height = this.scale.height;

    this.add.rectangle(width / 2, height / 2, width, height, 0x0a0a0f);

    this.add.text(width / 2, 10, 'Timeline', {
      fontSize: '16px',
      color: '#e2e8f0',
      fontFamily: 'monospace',
    }).setOrigin(0.5, 0);
  }

  updateBeads(beads: BeadData[]) {
    this.clearBeads();
    this.beads = beads;
    this.renderBeads();
  }

  private clearBeads() {
    this.beadGraphics.forEach(graphics => graphics.destroy());
    this.beadGraphics.clear();
  }

  private renderBeads() {
    const width = this.scale.width;
    const y = this.scale.height / 2;
    const startX = 50;
    const spacing = Math.min(100, (width - 100) / Math.max(1, this.beads.length));

    const emotionColors: Record<string, number> = {
      joy: 0x4ade80,
      sadness: 0x3b82f6,
      anger: 0xf87171,
      fear: 0xa78bfa,
      neutral: 0x94a3b8,
    };

    this.beads.forEach((bead, i) => {
      const x = startX + i * spacing + this.scrollOffset;
      const color = emotionColors[bead.emotion_tag || 'neutral'] || 0x94a3b8;

      const circle = this.add.circle(x, y, 8, color);
      circle.setInteractive();
      circle.on('pointerdown', () => this.selectBead(bead.id));

      if (i < this.beads.length - 1) {
        const nextX = startX + (i + 1) * spacing + this.scrollOffset;
        const line = this.add.graphics();
        line.lineStyle(2, 0x374151);
        line.lineBetween(x, y, nextX, y);
      }

      this.beadGraphics.set(bead.id, circle);
    });
  }

  private selectBead(beadId: string) {
    this.selectedIndex = beadId;
    this.events.emit('bead-selected', beadId);
  }

  getSelectedBead(): BeadData | null {
    if (!this.selectedIndex) return null;
    return this.beads.find(b => b.id === this.selectedIndex) || null;
  }
}
