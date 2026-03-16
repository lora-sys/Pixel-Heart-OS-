import { describe, it, expect } from 'vitest';
import { EventBus } from '../event-bus';

describe('EventBus', () => {
  it('should create instance', () => {
    const bus = new EventBus();
    expect(bus).toBeDefined();
  });

  it('should emit and listen to events', () => {
    const bus = new EventBus();
    let receivedData: any = null;

    bus.on('test-event', (data) => {
      receivedData = data;
    });

    bus.emit('test-event', { message: 'hello' });
    expect(receivedData).toEqual({ message: 'hello' });
  });

  it('should handle multiple listeners', () => {
    const bus = new EventBus();
    let count1 = 0;
    let count2 = 0;

    bus.on('multi-event', () => { count1++; });
    bus.on('multi-event', () => { count2++; });

    bus.emit('multi-event');
    expect(count1).toBe(1);
    expect(count2).toBe(1);
  });
});