"""
DVR Rules API endpoints.

Implements CRUD operations for DVR rules based on the design specification.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

from uhome_server.services.job_queue import get_job_queue, RecordingJob, JobStatus
from uhome_server.config import get_logger

_log = get_logger("uhome.dvr.rules")

router = APIRouter(prefix="/rules", tags=["dvr-rules"])


# Enums for rule types and other fixed values
class RuleType(str, Enum):
    time_based = "time-based"
    series = "series"
    movie = "movie"
    keyword = "keyword"
    channel = "channel"


class QualityProfile(str, Enum):
    sd = "sd"
    hd = "hd"
    uhd = "uhd"


class RecurrencePattern(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    custom = "custom"


# Pydantic models for request/response
class TimeBasedRuleCreate(BaseModel):
    rule_name: str
    rule_type: RuleType = RuleType.time_based
    channel_id: str
    start_time: datetime
    end_time: datetime
    recurrence: Optional[RecurrencePattern] = None
    program_title: Optional[str] = None
    quality_profile: QualityProfile = QualityProfile.hd
    priority: int = 3
    max_episodes: Optional[int] = None
    keep_until: Optional[datetime] = None


class SeriesRuleCreate(BaseModel):
    rule_name: str
    rule_type: RuleType = RuleType.series
    series_id: str
    series_title: str
    season_numbers: Optional[List[int]] = None
    include_specials: bool = False
    avoid_duplicates: bool = True
    quality_profile: QualityProfile = QualityProfile.hd
    priority: int = 3
    keep_until: Optional[datetime] = None


class MovieRuleCreate(BaseModel):
    rule_name: str
    rule_type: RuleType = RuleType.movie
    movie_id: str
    movie_title: str
    year: Optional[int] = None
    quality_profile: QualityProfile = QualityProfile.hd
    priority: int = 3
    keep_until: Optional[datetime] = None


class KeywordRuleCreate(BaseModel):
    rule_name: str
    rule_type: RuleType = RuleType.keyword
    keywords: List[str]
    require_all_keywords: bool = False
    channels: Optional[List[str]] = None
    time_ranges: Optional[List[str]] = None
    quality_profile: QualityProfile = QualityProfile.hd
    priority: int = 3
    keep_until: Optional[datetime] = None


class ChannelRuleCreate(BaseModel):
    rule_name: str
    rule_type: RuleType = RuleType.channel
    channel_id: str
    channel_name: str
    time_ranges: Optional[List[str]] = None
    quality_profile: QualityProfile = QualityProfile.hd
    priority: int = 3
    keep_until: Optional[datetime] = None


class DVRRuleResponse(BaseModel):
    rule_id: str
    rule_name: str
    rule_type: RuleType
    created_at: datetime
    updated_at: datetime
    enabled: bool
    priority: int
    status: str
    next_scheduled: Optional[datetime] = None


class DVRRuleListResponse(BaseModel):
    rules: List[DVRRuleResponse]
    total: int
    active: int
    disabled: int


# In-memory storage for rules (in production, this would be a database)
class DVRRuleStore:
    def __init__(self):
        self.rules = {}
        self.next_id = 1
        
    def create_rule(self, rule_data: dict) -> str:
        """Create a new DVR rule."""
        rule_id = f"rule_{self.next_id}"
        self.next_id += 1
        
        rule = {
            "rule_id": rule_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "enabled": True,
            "status": "active",
            **rule_data
        }
        
        self.rules[rule_id] = rule
        return rule_id
        
    def get_rule(self, rule_id: str) -> Optional[dict]:
        """Get a rule by ID."""
        return self.rules.get(rule_id)
        
    def list_rules(self) -> List[dict]:
        """List all rules."""
        return list(self.rules.values())
        
    def update_rule(self, rule_id: str, updates: dict) -> bool:
        """Update a rule."""
        if rule_id not in self.rules:
            return False
        
        self.rules[rule_id].update(updates)
        self.rules[rule_id]["updated_at"] = datetime.now()
        return True
        
    def delete_rule(self, rule_id: str) -> bool:
        """Delete a rule."""
        if rule_id not in self.rules:
            return False
        
        del self.rules[rule_id]
        return True
        
    def enable_rule(self, rule_id: str) -> bool:
        """Enable a rule."""
        if rule_id not in self.rules:
            return False
        
        self.rules[rule_id]["enabled"] = True
        self.rules[rule_id]["updated_at"] = datetime.now()
        return True
        
    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule."""
        if rule_id not in self.rules:
            return False
        
        self.rules[rule_id]["enabled"] = False
        self.rules[rule_id]["updated_at"] = datetime.now()
        return True


# Global rule store instance
rule_store = DVRRuleStore()


@router.post("/", response_model=DVRRuleResponse)
async def create_rule(rule_data: dict):
    """
    Create a new DVR rule.
    
    Supports all rule types: time-based, series, movie, keyword, channel
    """
    try:
        # Validate rule type
        rule_type = rule_data.get("rule_type")
        if rule_type not in [rt.value for rt in RuleType]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid rule type"
            )
        
        # Create the rule
        rule_id = rule_store.create_rule(rule_data)
        rule = rule_store.get_rule(rule_id)
        
        # Schedule the rule (create job if applicable)
        if rule_type in [RuleType.time_based.value, RuleType.series.value]:
            job_queue = get_job_queue()
            
            # Create a recording job for time-based rules
            if rule_type == RuleType.time_based.value:
                recording_job = RecordingJob(
                    job_id=f"job_{rule_id}",
                    job_type="recording",
                    status=JobStatus.QUEUED,
                    priority=rule_data.get("priority", 3),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    params={},
                    rule_id=rule_id,
                    channel_id=rule_data.get("channel_id", "unknown"),
                    start_time=rule_data.get("start_time", datetime.now()),
                    end_time=rule_data.get("end_time", datetime.now()),
                    quality_profile=rule_data.get("quality_profile", "hd")
                )
                job_queue.add_job(recording_job)
                _log.info(f"Created recording job for rule {rule_id}")
        
        return DVRRuleResponse(
            rule_id=rule_id,
            rule_name=rule["rule_name"],
            rule_type=rule["rule_type"],
            created_at=rule["created_at"],
            updated_at=rule["updated_at"],
            enabled=rule["enabled"],
            priority=rule["priority"],
            status=rule["status"],
            next_scheduled=rule_data.get("start_time") if rule_type == RuleType.time_based.value else None
        )
        
    except Exception as e:
        _log.error(f"Failed to create DVR rule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create rule: {str(e)}"
        )


@router.get("/", response_model=DVRRuleListResponse)
async def list_rules(enabled: Optional[bool] = None, rule_type: Optional[str] = None):
    """
    List all DVR rules.
    
    Optional filters: enabled status, rule type
    """
    rules = rule_store.list_rules()
    
    # Apply filters
    if enabled is not None:
        rules = [r for r in rules if r["enabled"] == enabled]
    
    if rule_type:
        rules = [r for r in rules if r["rule_type"] == rule_type]
    
    # Count active/disabled
    active_count = sum(1 for r in rules if r["enabled"])
    disabled_count = len(rules) - active_count
    
    return DVRRuleListResponse(
        rules=[DVRRuleResponse(
            rule_id=r["rule_id"],
            rule_name=r["rule_name"],
            rule_type=r["rule_type"],
            created_at=r["created_at"],
            updated_at=r["updated_at"],
            enabled=r["enabled"],
            priority=r.get("priority", 3),
            status=r["status"],
            next_scheduled=r.get("start_time") if r["rule_type"] == RuleType.time_based.value else None
        ) for r in rules],
        total=len(rules),
        active=active_count,
        disabled=disabled_count
    )


@router.get("/{rule_id}", response_model=DVRRuleResponse)
async def get_rule(rule_id: str):
    """
    Get a specific DVR rule by ID.
    """
    rule = rule_store.get_rule(rule_id)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    return DVRRuleResponse(
        rule_id=rule["rule_id"],
        rule_name=rule["rule_name"],
        rule_type=rule["rule_type"],
        created_at=rule["created_at"],
        updated_at=rule["updated_at"],
        enabled=rule["enabled"],
        priority=rule.get("priority", 3),
        status=rule["status"],
        next_scheduled=rule.get("start_time") if rule["rule_type"] == RuleType.time_based.value else None
    )


@router.put("/{rule_id}", response_model=DVRRuleResponse)
async def update_rule(rule_id: str, updates: dict):
    """
    Update a DVR rule.
    """
    rule = rule_store.get_rule(rule_id)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    # Update the rule
    success = rule_store.update_rule(rule_id, updates)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update rule"
        )
    
    # Get updated rule
    updated_rule = rule_store.get_rule(rule_id)
    
    return DVRRuleResponse(
        rule_id=updated_rule["rule_id"],
        rule_name=updated_rule["rule_name"],
        rule_type=updated_rule["rule_type"],
        created_at=updated_rule["created_at"],
        updated_at=updated_rule["updated_at"],
        enabled=updated_rule["enabled"],
        priority=updated_rule.get("priority", 3),
        status=updated_rule["status"],
        next_scheduled=updated_rule.get("start_time") if updated_rule["rule_type"] == RuleType.time_based.value else None
    )


@router.delete("/{rule_id}")
async def delete_rule(rule_id: str):
    """
    Delete a DVR rule.
    """
    rule = rule_store.get_rule(rule_id)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    # Delete the rule
    success = rule_store.delete_rule(rule_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete rule"
        )
    
    return {"success": True, "message": "Rule deleted successfully"}


@router.post("/{rule_id}/enable")
async def enable_rule(rule_id: str):
    """
    Enable a DVR rule.
    """
    success = rule_store.enable_rule(rule_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    return {"success": True, "message": "Rule enabled"}


@router.post("/{rule_id}/disable")
async def disable_rule(rule_id: str):
    """
    Disable a DVR rule.
    """
    success = rule_store.disable_rule(rule_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    return {"success": True, "message": "Rule disabled"}


@router.post("/test-recording")
async def test_recording(test_data: dict):
    """
    Test recording endpoint for debugging.
    """
    channel = test_data.get("channel", "test-channel")
    duration = test_data.get("duration", 60)  # seconds
    
    _log.info(f"Starting test recording on {channel} for {duration} seconds")
    
    # In a real implementation, this would start an actual recording
    # For now, we'll just log and return success
    
    return {
        "success": True,
        "message": f"Test recording started on {channel}",
        "duration": duration,
        "recording_id": f"test_rec_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }