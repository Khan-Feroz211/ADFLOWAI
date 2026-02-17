"""
ADFLOWAI - Advanced Real-Time Campaign Monitor
Real-time streaming analytics with WebSocket support
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Set
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class RealTimeMetrics:
    """Real-time campaign metrics"""
    campaign_id: int
    timestamp: str
    impressions_per_second: float
    clicks_per_second: float
    spend_rate: float
    current_ctr: float
    current_cpc: float
    performance_score: float
    prediction_next_hour: Dict
    alerts: List[Dict]
    recommendations: List[str]


class RealTimeMonitor:
    """
    Advanced real-time monitoring system
    
    Features:
    - WebSocket streaming
    - Live performance tracking
    - Anomaly detection in real-time
    - Predictive alerts
    - Auto-scaling recommendations
    """
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.active_campaigns: Set[int] = set()
        self.websocket_clients: Set = set()
        self.alert_thresholds = {
            'ctr_drop': 0.20,  # 20% drop triggers alert
            'cpc_spike': 0.30,  # 30% increase triggers alert
            'spend_rate_high': 0.90,  # 90% of budget spent
            'performance_drop': 0.40  # Performance score drops below 0.4
        }
        
        logger.info("Real-time monitor initialized")
    
    async def start_monitoring(self, campaign_id: int):
        """
        Start real-time monitoring for a campaign
        
        Args:
            campaign_id: Campaign to monitor
        """
        self.active_campaigns.add(campaign_id)
        logger.info(f"Started real-time monitoring for campaign {campaign_id}")
        
        # Start monitoring loop
        asyncio.create_task(self._monitor_loop(campaign_id))
    
    async def stop_monitoring(self, campaign_id: int):
        """Stop monitoring a campaign"""
        self.active_campaigns.discard(campaign_id)
        logger.info(f"Stopped monitoring campaign {campaign_id}")
    
    async def _monitor_loop(self, campaign_id: int):
        """
        Main monitoring loop - runs continuously
        
        Collects metrics every second and streams to clients
        """
        while campaign_id in self.active_campaigns:
            try:
                # Collect real-time metrics
                metrics = await self._collect_metrics(campaign_id)
                
                # Check for anomalies
                alerts = await self._detect_anomalies(campaign_id, metrics)
                
                # Generate predictions
                predictions = await self._generate_predictions(campaign_id, metrics)
                
                # Create real-time update
                update = RealTimeMetrics(
                    campaign_id=campaign_id,
                    timestamp=datetime.utcnow().isoformat(),
                    impressions_per_second=metrics.get('impressions_rate', 0),
                    clicks_per_second=metrics.get('clicks_rate', 0),
                    spend_rate=metrics.get('spend_rate', 0),
                    current_ctr=metrics.get('ctr', 0),
                    current_cpc=metrics.get('cpc', 0),
                    performance_score=metrics.get('performance_score', 0.5),
                    prediction_next_hour=predictions,
                    alerts=alerts,
                    recommendations=await self._generate_recommendations(metrics, alerts)
                )
                
                # Stream to WebSocket clients
                await self._broadcast_update(update)
                
                # Cache in Redis for dashboards
                if self.redis:
                    await self._cache_metrics(campaign_id, update)
                
                # Wait before next collection
                await asyncio.sleep(1)  # Update every second
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(5)  # Wait longer on error
    
    async def _collect_metrics(self, campaign_id: int) -> Dict:
        """
        Collect current metrics from platform APIs
        
        In production, this would call actual platform APIs
        For now, simulate with realistic data
        """
        # TODO: Replace with actual API calls
        import random
        
        return {
            'impressions_rate': random.uniform(10, 100),
            'clicks_rate': random.uniform(0.1, 5),
            'spend_rate': random.uniform(0.5, 10),
            'ctr': random.uniform(0.01, 0.05),
            'cpc': random.uniform(0.5, 3.0),
            'performance_score': random.uniform(0.3, 0.9)
        }
    
    async def _detect_anomalies(self, campaign_id: int, metrics: Dict) -> List[Dict]:
        """
        Detect anomalies in real-time using statistical methods
        
        Returns list of alerts with severity levels
        """
        alerts = []
        
        # CTR anomaly detection
        if metrics.get('ctr', 0) < 0.01:  # Below 1%
            alerts.append({
                'type': 'ctr_low',
                'severity': 'warning',
                'message': f"CTR unusually low: {metrics['ctr']*100:.2f}%",
                'threshold': '1%',
                'action_required': 'Review ad creative and targeting'
            })
        
        # CPC spike detection
        if metrics.get('cpc', 0) > 5.0:  # Above $5
            alerts.append({
                'type': 'cpc_high',
                'severity': 'critical',
                'message': f"CPC spike detected: ${metrics['cpc']:.2f}",
                'threshold': '$5.00',
                'action_required': 'Consider pausing campaign'
            })
        
        # Performance drop
        if metrics.get('performance_score', 1.0) < 0.4:
            alerts.append({
                'type': 'performance_drop',
                'severity': 'critical',
                'message': f"Performance score dropped to {metrics['performance_score']:.2f}",
                'threshold': '0.40',
                'action_required': 'Immediate optimization needed'
            })
        
        # Budget burn rate
        if metrics.get('spend_rate', 0) > 15:  # Spending too fast
            alerts.append({
                'type': 'high_spend_rate',
                'severity': 'warning',
                'message': f"High spend rate: ${metrics['spend_rate']:.2f}/hour",
                'threshold': '$15/hour',
                'action_required': 'Monitor budget closely'
            })
        
        return alerts
    
    async def _generate_predictions(self, campaign_id: int, metrics: Dict) -> Dict:
        """
        Generate predictions for next hour using time series models
        
        In production, this would use trained LSTM/Prophet models
        """
        # TODO: Replace with actual ML model predictions
        current_ctr = metrics.get('ctr', 0.02)
        current_spend = metrics.get('spend_rate', 5.0)
        
        # Simple trend-based prediction (replace with ML)
        predicted_impressions = metrics.get('impressions_rate', 50) * 3600  # Next hour
        predicted_clicks = predicted_impressions * current_ctr
        predicted_spend = current_spend * 1.0  # Assume constant rate
        
        return {
            'next_hour': {
                'impressions': int(predicted_impressions),
                'clicks': int(predicted_clicks),
                'estimated_spend': round(predicted_spend, 2),
                'projected_ctr': round(current_ctr * 100, 2),
                'confidence': 0.85  # Model confidence
            },
            'end_of_day': {
                'total_impressions': int(predicted_impressions * 8),  # 8 hours remaining
                'total_clicks': int(predicted_clicks * 8),
                'total_spend': round(predicted_spend * 8, 2)
            }
        }
    
    async def _generate_recommendations(self, metrics: Dict, alerts: List[Dict]) -> List[str]:
        """
        Generate actionable recommendations based on current state
        """
        recommendations = []
        
        performance = metrics.get('performance_score', 0.5)
        ctr = metrics.get('ctr', 0)
        cpc = metrics.get('cpc', 0)
        
        # Performance-based recommendations
        if performance < 0.4:
            recommendations.append("🔴 URGENT: Consider pausing campaign - performance is critically low")
        elif performance < 0.6:
            recommendations.append("⚠️ Optimize ad creative and targeting to improve performance")
        elif performance > 0.8:
            recommendations.append("✅ Campaign performing excellently - consider increasing budget")
        
        # CTR recommendations
        if ctr < 0.015:
            recommendations.append("💡 Low CTR: Test new ad copy and visuals")
        elif ctr > 0.04:
            recommendations.append("🎯 Excellent CTR: Allocate more budget to this campaign")
        
        # CPC recommendations
        if cpc > 4.0:
            recommendations.append("💰 High CPC: Refine audience targeting to reduce costs")
        elif cpc < 1.0:
            recommendations.append("💎 Great CPC: Scale up campaign spend")
        
        # Alert-based recommendations
        for alert in alerts:
            if alert['severity'] == 'critical':
                recommendations.insert(0, f"🚨 {alert['action_required']}")
        
        return recommendations[:5]  # Top 5 recommendations
    
    async def _broadcast_update(self, update: RealTimeMetrics):
        """
        Broadcast update to all connected WebSocket clients
        """
        message = json.dumps(asdict(update))
        
        # Send to all connected clients
        for client in self.websocket_clients:
            try:
                await client.send(message)
            except Exception as e:
                logger.error(f"Failed to send to client: {str(e)}")
                self.websocket_clients.discard(client)
    
    async def _cache_metrics(self, campaign_id: int, metrics: RealTimeMetrics):
        """
        Cache metrics in Redis for dashboard retrieval
        """
        if not self.redis:
            return
        
        key = f"realtime:campaign:{campaign_id}"
        value = json.dumps(asdict(metrics))
        
        # Store with 5-minute expiration
        await self.redis.setex(key, 300, value)
    
    def register_websocket_client(self, websocket):
        """Register a new WebSocket client"""
        self.websocket_clients.add(websocket)
        logger.info(f"WebSocket client registered. Total: {len(self.websocket_clients)}")
    
    def unregister_websocket_client(self, websocket):
        """Unregister a WebSocket client"""
        self.websocket_clients.discard(websocket)
        logger.info(f"WebSocket client unregistered. Total: {len(self.websocket_clients)}")
    
    async def get_current_metrics(self, campaign_id: int) -> Dict:
        """
        Get current cached metrics for a campaign
        
        Used by REST API for polling-based clients
        """
        if not self.redis:
            return {}
        
        key = f"realtime:campaign:{campaign_id}"
        cached = await self.redis.get(key)
        
        if cached:
            return json.loads(cached)
        
        return {}
    
    def get_active_campaigns(self) -> List[int]:
        """Get list of actively monitored campaigns"""
        return list(self.active_campaigns)


# Global monitor instance
monitor = RealTimeMonitor()
