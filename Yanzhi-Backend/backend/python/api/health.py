#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
健康检查模块
提供系统健康状态监控
"""

from fastapi import APIRouter
import psutil
import platform

router = APIRouter()


@router.get("/")
async def health_check():
    """
    基本健康检查
    """
    return {
        "code": 200,
        "message": "系统运行正常",
        "data": {
            "status": "healthy",
            "timestamp": __import__("time").time()
        }
    }


@router.get("/detailed")
async def detailed_health_check():
    """
    详细健康检查
    """
    try:
        # 获取系统信息
        cpu_info = {
            "usage_percent": psutil.cpu_percent(interval=1),
            "core_count": psutil.cpu_count(logical=False),
            "thread_count": psutil.cpu_count(logical=True)
        }
        
        memory_info = {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent
        }
        
        disk_info = {
            "total": psutil.disk_usage('/').total,
            "used": psutil.disk_usage('/').used,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent
        }
        
        system_info = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "architecture": platform.machine()
        }
        
        return {
            "code": 200,
            "message": "系统状态正常",
            "data": {
                "status": "healthy",
                "cpu": cpu_info,
                "memory": memory_info,
                "disk": disk_info,
                "system": system_info,
                "timestamp": __import__("time").time()
            }
        }
        
    except Exception as e:
        return {
            "code": 500,
            "message": f"健康检查失败: {str(e)}",
            "data": {
                "status": "unhealthy",
                "error": str(e)
            }
        }