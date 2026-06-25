package com.example.backend.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDate;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class Subsidy {

    private String id;
    
    private String title;

    private String description;

    private Double amount;

    private String eligibilityCriteria;

    private String applicationDeadline;
    
    private String state; // e.g., "Maharashtra", "Central", "Bihar"
    
    private String category; // e.g., "Agriculture", "Education", "Women Empowerment"

    private boolean isActive = true;

    private String applicationUrl; // URL for official application portal

    private java.util.List<String> documentsRequired;
}
