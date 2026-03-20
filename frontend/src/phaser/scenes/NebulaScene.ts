import { Scene } from 'phaser';

export class NebulaScene extends Scene {
  private nodes: Map<string, any> = new Map();
  private edges: any[] = [];

  constructor() {
    super({ key: 'NebulaScene' });
  }

  create() {
    const width = this.scale.width;
    const height = this.scale.height;

    this.add.rectangle(width / 2, height / 2, width, height, 0x0a0a0f);

    this.add.text(width / 2, 20, 'Relationship Nebula', {
      fontSize: '18px',
      color: '#e2e8f0',
      fontFamily: 'monospace',
    }).setOrigin(0.5, 0);
  }

  addNPCNode(id: string, name: string, archetype: string, x: number, y: number) {
    const colors: Record<string, number> = {
      protector: 0x4ade80,
      competitor: 0xf87171,
      shadow: 0xa78bfa,
      ally: 0x3b82f6,
      mentor: 0xec4899,
    };

    const color = colors[archetype] || 0x94a3b8;

    const circle = this.add.circle(x, y, 20, color);
    const label = this.add.text(x, y + 30, name, {
      fontSize: '12px',
      color: '#e2e8f0',
      fontFamily: 'monospace',
    }).setOrigin(0.5, 0);

    this.nodes.set(id, { circle, label, name, archetype });
  }

  addEdge(fromId: string, toId: string, strength: number) {
    const from = this.nodes.get(fromId);
    const to = this.nodes.get(toId);

    if (!from || !to) return;

    const line = this.add.graphics();
    const alpha = Math.abs(strength);
    const color = strength > 0 ? 0x4ade80 : 0xf87171;

    line.lineStyle(2, color, alpha);
    line.lineBetween(
      from.circle.x, from.circle.y,
      to.circle.x, to.circle.y
    );

    this.edges.push({ line, fromId, toId, strength });
  }

  clear() {
    this.nodes.forEach(node => {
      node.circle.destroy();
      node.label.destroy();
    });
    this.nodes.clear();

    this.edges.forEach(edge => edge.line.destroy());
    this.edges = [];
  }
}
