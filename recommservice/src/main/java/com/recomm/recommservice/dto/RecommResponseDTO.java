package com.recomm.recommservice.dto;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

public class RecommResponseDTO {

    @JsonProperty("recommendations")
    private List<String> placeIds;

    public List<String> getPlaceIds() {
    return placeIds;
}

public void setPlaceId(List<String> placeIds) {
    this.placeIds = placeIds;
}
}
