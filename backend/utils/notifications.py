"""
Notification System - Alerts via SMS/Email
"""
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class NotificationManager:
    """
    Manages alerts and notifications
    SMS, Email, and future integrations (Telegram, Discord, etc.)
    """
    
    def __init__(
        self,
        email_enabled: bool = False,
        smtp_server: Optional[str] = None,
        smtp_port: int = 587,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None,
        from_email: Optional[str] = None,
        to_email: Optional[str] = None
    ):
        self.email_enabled = email_enabled
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.to_email = to_email
        
        if email_enabled:
            logger.info("📧 Email notifications enabled")
    
    async def send_email(self, subject: str, body: str, html: bool = False):
        """Send email notification"""
        if not self.email_enabled:
            logger.debug("Email notifications disabled")
            return
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            
            if html:
                part = MIMEText(body, 'html')
            else:
                part = MIMEText(body, 'plain')
            
            msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"📧 Email sent: {subject}")
        
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    
    async def send_trade_alert(self, trade_data: dict):
        """Send trade execution alert"""
        subject = f"🤖 QuantumTrade: {trade_data['side'].upper()} {trade_data['symbol']}"
        body = f"""
Trade Executed:
--------------
Side: {trade_data['side'].upper()}
Symbol: {trade_data['symbol']}
Quantity: {trade_data['quantity']}
Price: ${trade_data['price']:.2f}
Order ID: {trade_data['order_id']}
Strategy: {trade_data.get('strategy', 'N/A')}

Total Value: ${trade_data['quantity'] * trade_data['price']:.2f}
        """
        
        await self.send_email(subject, body)
    
    async def send_risk_alert(self, alert_type: str, message: str):
        """Send risk management alert"""
        subject = f"⚠️  QuantumTrade Risk Alert: {alert_type}"
        body = f"""
Risk Alert Triggered:
-------------------
Type: {alert_type}
Message: {message}

Please review your positions and trading strategy.
        """
        
        await self.send_email(subject, body)
    
    async def send_daily_summary(self, summary_data: dict):
        """Send daily trading summary"""
        subject = f"📊 QuantumTrade Daily Summary"
        body = f"""
Daily Trading Summary:
--------------------
Date: {summary_data['date']}

Performance:
- Total P&L: ${summary_data['total_pnl']:.2f} ({summary_data['pnl_pct']:.2f}%)
- Trades Today: {summary_data['trades_count']}
- Win Rate: {summary_data['win_rate']:.2f}%

Portfolio:
- Current Balance: ${summary_data['current_balance']:.2f}
- Open Positions: {summary_data['open_positions']}

Risk Metrics:
- Daily Drawdown: {summary_data['daily_drawdown']:.2f}%
- Circuit Breaker: {'ACTIVE' if summary_data['circuit_breaker'] else 'Inactive'}
        """
        
        await self.send_email(subject, body)