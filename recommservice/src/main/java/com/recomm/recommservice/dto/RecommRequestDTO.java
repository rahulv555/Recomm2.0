package com.recomm.recommservice.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class RecommRequestDTO {

@JsonProperty("latitude")
private Double latitude;

@JsonProperty("longitude")
private Double longitude;


    public Double getLatitude() {
    return latitude;
}

public void setLatitude(Double latitude) {
    this.latitude = latitude;
}

public Double getLongitude() {
    return longitude;
}

public void setLongitude(Double longitude) {
    this.longitude = longitude;
}
}
