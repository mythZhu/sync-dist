#!/usr/bin/env python


class DistributionError(Exception):
    pass


class LocationError(DistributionError):
    pass


class MetadataError(DistributionError):
    pass
