package com.example.backend.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class Application {
    private String id;
    private String schemeId;
    private String schemeTitle;
    private String applicantName;
    private String applicantAadhar;
    private String applicantState;
    private String applicantIncome;
    private String status; // e.g. "PENDING", "APPROVED", "REJECTED"
    private String submittedAt;
}
