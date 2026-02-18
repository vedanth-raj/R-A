"""
Performance Monitoring and Metrics Module for Text Extraction System

This module provides comprehensive performance monitoring, metrics collection,
and analysis capabilities for the text extraction pipeline.

Features:
- Real-time performance metrics
- Memory usage monitoring
- Processing time tracking
- Resource utilization analysis
- Performance bottleneck detection
- Automated performance reports
- Performance trend analysis
"""

import time
import psutil
import threading
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, deque
from datetime import datetime, timedelta
import functools
import sys

@dataclass
class PerformanceMetric:
    """Single performance metric data point."""
    name: str
    value: float
    unit: str
    timestamp: float
    context: Dict[str, Any] = None

@dataclass
class ProcessingStats:
    """Statistics for a processing operation."""
    operation_name: str
    start_time: float
    end_time: float
    duration: float
    memory_before: float
    memory_after: float
    memory_peak: float
    cpu_percent: float
    success: bool
    error_message: Optional[str] = None
    input_size: Optional[int] = None
    output_size: Optional[int] = None

class PerformanceMonitor:
    """Comprehensive performance monitoring system."""
    
    def __init__(self, metrics_file: str = "performance_metrics.json"):
        """Initialize the performance monitor."""
        self.metrics_file = metrics_file
        self.metrics: List[PerformanceMetric] = []
        self.processing_stats: List[ProcessingStats] = []
        self.active_operations: Dict[str, float] = {}
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Performance thresholds
        self.thresholds = {
            'memory_warning': 1024 * 1024 * 1024,  # 1GB
            'memory_critical': 2 * 1024 * 1024 * 1024,  # 2GB
            'processing_time_warning': 300,  # 5 minutes
            'processing_time_critical': 600,  # 10 minutes
            'cpu_warning': 80,  # 80%
            'cpu_critical': 95  # 95%
        }
        
        # Setup logging
        self.logger = logging.getLogger('performance_monitor')
        self.setup_logging()
        
        # Start background monitoring
        self.start_monitoring()
    
    def setup_logging(self):
        """Setup performance monitoring logging."""
        import os
        try:
            log_file = '/tmp/performance_monitor.log' if os.environ.get('VERCEL') else 'performance_monitor.log'
            handler = logging.FileHandler(log_file, encoding='utf-8')
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        except (OSError, PermissionError):
            # Skip file logging on read-only filesystems
            pass
        self.logger.setLevel(logging.INFO)
    
    def start_monitoring(self):
        """Start background performance monitoring."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop background performance monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Background monitoring loop."""
        while self.monitoring_active:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Check for performance issues
                self._check_performance_thresholds()
                
                # Sleep for monitoring interval
                time.sleep(10)  # Monitor every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)  # Wait longer on error
    
    def _collect_system_metrics(self):
        """Collect system performance metrics."""
        current_time = time.time()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        self.add_metric("memory_used", memory.used, "bytes", current_time)
        self.add_metric("memory_percent", memory.percent, "percent", current_time)
        self.add_metric("memory_available", memory.available, "bytes", current_time)
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        self.add_metric("cpu_percent", cpu_percent, "percent", current_time)
        
        # Process-specific metrics
        process = psutil.Process()
        process_memory = process.memory_info()
        self.add_metric("process_memory_rss", process_memory.rss, "bytes", current_time)
        self.add_metric("process_memory_vms", process_memory.vms, "bytes", current_time)
        self.add_metric("process_cpu_percent", process.cpu_percent(), "percent", current_time)
        
        # Disk metrics
        disk = psutil.disk_usage('.')
        self.add_metric("disk_used", disk.used, "bytes", current_time)
        self.add_metric("disk_percent", (disk.used / disk.total) * 100, "percent", current_time)
    
    def _check_performance_thresholds(self):
        """Check performance thresholds and log warnings."""
        current_metrics = self.get_latest_metrics()
        
        # Check memory usage
        memory_percent = current_metrics.get("memory_percent", 0)
        if memory_percent > self.thresholds['cpu_critical']:
            self.logger.critical(f"Critical memory usage: {memory_percent:.1f}%")
        elif memory_percent > self.thresholds['cpu_warning']:
            self.logger.warning(f"High memory usage: {memory_percent:.1f}%")
        
        # Check CPU usage
        cpu_percent = current_metrics.get("cpu_percent", 0)
        if cpu_percent > self.thresholds['cpu_critical']:
            self.logger.critical(f"Critical CPU usage: {cpu_percent:.1f}%")
        elif cpu_percent > self.thresholds['cpu_warning']:
            self.logger.warning(f"High CPU usage: {cpu_percent:.1f}%")
        
        # Check long-running operations
        current_time = time.time()
        for operation, start_time in self.active_operations.items():
            duration = current_time - start_time
            if duration > self.thresholds['processing_time_critical']:
                self.logger.critical(f"Operation '{operation}' running for {duration:.1f}s (critical)")
            elif duration > self.thresholds['processing_time_warning']:
                self.logger.warning(f"Operation '{operation}' running for {duration:.1f}s (warning)")
    
    def add_metric(self, name: str, value: float, unit: str, timestamp: Optional[float] = None, 
                   context: Dict[str, Any] = None):
        """Add a performance metric."""
        if timestamp is None:
            timestamp = time.time()
        
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=timestamp,
            context=context or {}
        )
        
        self.metrics.append(metric)
        
        # Keep only recent metrics (last 24 hours)
        cutoff_time = time.time() - (24 * 60 * 60)
        self.metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
    
    def start_operation(self, operation_name: str) -> str:
        """Start monitoring an operation."""
        operation_id = f"{operation_name}_{int(time.time() * 1000)}"
        self.active_operations[operation_id] = time.time()
        return operation_id
    
    def end_operation(self, operation_id: str, operation_name: str, success: bool = True,
                      error_message: Optional[str] = None, input_size: Optional[int] = None,
                      output_size: Optional[int] = None) -> ProcessingStats:
        """End monitoring an operation and record statistics."""
        if operation_id not in self.active_operations:
            raise ValueError(f"Operation {operation_id} not found")
        
        start_time = self.active_operations.pop(operation_id)
        end_time = time.time()
        duration = end_time - start_time
        
        # Get memory metrics
        process = psutil.Process()
        memory_info = process.memory_info()
        
        stats = ProcessingStats(
            operation_name=operation_name,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            memory_before=0,  # Would need to track this separately
            memory_after=memory_info.rss,
            memory_peak=memory_info.rss,  # Simplified
            cpu_percent=process.cpu_percent(),
            success=success,
            error_message=error_message,
            input_size=input_size,
            output_size=output_size
        )
        
        self.processing_stats.append(stats)
        
        # Log operation completion
        if success:
            self.logger.info(f"Operation '{operation_name}' completed in {duration:.2f}s")
        else:
            self.logger.error(f"Operation '{operation_name}' failed after {duration:.2f}s: {error_message}")
        
        return stats
    
    def get_latest_metrics(self, count: int = 100) -> Dict[str, float]:
        """Get the latest metrics."""
        latest_metrics = {}
        recent_metrics = sorted(self.metrics, key=lambda m: m.timestamp, reverse=True)[:count]
        
        for metric in recent_metrics:
            if metric.name not in latest_metrics:
                latest_metrics[metric.name] = metric.value
        
        return latest_metrics
    
    def get_operation_stats(self, operation_name: Optional[str] = None) -> List[ProcessingStats]:
        """Get processing statistics."""
        if operation_name:
            return [s for s in self.processing_stats if s.operation_name == operation_name]
        return self.processing_stats.copy()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        # System metrics
        current_metrics = self.get_latest_metrics()
        
        # Operation statistics
        total_operations = len(self.processing_stats)
        successful_operations = len([s for s in self.processing_stats if s.success])
        failed_operations = total_operations - successful_operations
        
        # Performance calculations
        if self.processing_stats:
            avg_duration = sum(s.duration for s in self.processing_stats) / len(self.processing_stats)
            max_duration = max(s.duration for s in self.processing_stats)
            min_duration = min(s.duration for s in self.processing_stats)
        else:
            avg_duration = max_duration = min_duration = 0
        
        # Memory usage
        memory_percent = current_metrics.get("memory_percent", 0)
        process_memory = current_metrics.get("process_memory_rss", 0)
        
        # CPU usage
        cpu_percent = current_metrics.get("cpu_percent", 0)
        
        return {
            'timestamp': time.time(),
            'system_metrics': {
                'memory_percent': memory_percent,
                'process_memory_mb': process_memory / (1024 * 1024),
                'cpu_percent': cpu_percent
            },
            'operation_stats': {
                'total_operations': total_operations,
                'successful_operations': successful_operations,
                'failed_operations': failed_operations,
                'success_rate': successful_operations / total_operations if total_operations > 0 else 0,
                'avg_duration_seconds': avg_duration,
                'max_duration_seconds': max_duration,
                'min_duration_seconds': min_duration
            },
            'active_operations': len(self.active_operations),
            'metrics_collected': len(self.metrics)
        }
    
    def detect_performance_bottlenecks(self) -> List[Dict[str, Any]]:
        """Detect performance bottlenecks."""
        bottlenecks = []
        
        # Check slow operations
        if self.processing_stats:
            avg_duration = sum(s.duration for s in self.processing_stats) / len(self.processing_stats)
            
            for stat in self.processing_stats:
                if stat.duration > avg_duration * 2:  # More than 2x average
                    bottlenecks.append({
                        'type': 'slow_operation',
                        'operation': stat.operation_name,
                        'duration': stat.duration,
                        'avg_duration': avg_duration,
                        'severity': 'high' if stat.duration > avg_duration * 3 else 'medium'
                    })
        
        # Check memory usage trends
        recent_metrics = [m for m in self.metrics if m.name == "memory_percent" and 
                         m.timestamp > time.time() - 3600]  # Last hour
        
        if len(recent_metrics) > 10:
            memory_trend = self._calculate_trend([m.value for m in recent_metrics])
            if memory_trend > 5:  # Increasing trend
                bottlenecks.append({
                    'type': 'memory_leak',
                    'trend': memory_trend,
                    'severity': 'high' if memory_trend > 10 else 'medium'
                })
        
        # Check high CPU usage
        current_cpu = self.get_latest_metrics().get("cpu_percent", 0)
        if current_cpu > self.thresholds['cpu_warning']:
            bottlenecks.append({
                'type': 'high_cpu',
                'cpu_percent': current_cpu,
                'severity': 'critical' if current_cpu > self.thresholds['cpu_critical'] else 'high'
            })
        
        return bottlenecks
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend (slope) of values."""
        if len(values) < 2:
            return 0
        
        n = len(values)
        x = list(range(n))
        
        # Calculate linear regression slope
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope
    
    def save_performance_report(self, output_path: str):
        """Save comprehensive performance report."""
        report = {
            'generated_at': time.time(),
            'summary': self.get_performance_summary(),
            'bottlenecks': self.detect_performance_bottlenecks(),
            'recent_metrics': [asdict(m) for m in self.metrics[-100:]],  # Last 100 metrics
            'operation_stats': [asdict(s) for s in self.processing_stats[-50:]]  # Last 50 operations
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Performance report saved to {output_path}")
    
    def clear_old_data(self, days_to_keep: int = 7):
        """Clear old performance data."""
        cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
        
        # Clear old metrics
        self.metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
        
        # Clear old processing stats
        self.processing_stats = [s for s in self.processing_stats if s.end_time > cutoff_time]
        
        self.logger.info(f"Cleared performance data older than {days_to_keep} days")


# Global performance monitor instance
global_performance_monitor = PerformanceMonitor()

def monitor_performance(operation_name: str):
    """Decorator to monitor function performance."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Start monitoring
            operation_id = global_performance_monitor.start_operation(operation_name)
            
            try:
                # Execute function
                result = func(*args, **kwargs)
                
                # End monitoring successfully
                global_performance_monitor.end_operation(operation_id, operation_name, success=True)
                
                return result
                
            except Exception as e:
                # End monitoring with error
                global_performance_monitor.end_operation(
                    operation_id, operation_name, success=False, error_message=str(e)
                )
                raise
        
        return wrapper
    return decorator

def get_performance_summary() -> Dict[str, Any]:
    """Get current performance summary."""
    return global_performance_monitor.get_performance_summary()

def save_performance_report(output_path: str = "performance_report.json"):
    """Save performance report."""
    global_performance_monitor.save_performance_report(output_path)
