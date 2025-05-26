#include <stdint.h>

#pragma once
#pragma pack(push,1)
typedef struct {
	// at -> auxiliary traces, dt -> data traces
	int32_t job_id_number; //3201 ~ 3204
	int32_t line_number; // 3205 ~
	int32_t reel_number; // 3209
	int16_t num_of_dt_per_ensemble; // 3213
	int16_t num_of_at_per_ensemble; // 3215
	int16_t sample_interval; // 3217
	int16_t origin_interval; // 3219
	int16_t num_of_samples_per_dt; // 3221
	int16_t origin_num_of_samples_per_dt; // 3223
	int16_t format_code; // 3225
	int16_t ensemble_fold; // 3227
	int16_t trace_sorting_code; // 3229
	int16_t vertical_sum_code; // 3231
	int16_t start_sweep_freq; // 3233
	int16_t end_sweep_freq; // 3235
	int16_t sweep_len; // 3237
	int16_t sweep_type; // 3239
	int16_t num_of_sweep_ch; // 3241
	int16_t start_taper_len; // 3243
	int16_t end_taper_len; // 3245
	int16_t taper_Type; // 3247
	int16_t correlated; // 3249
	int16_t bin_gain_recoverd; // 3251
	int16_t amp_recovered_method; // 3253
	int16_t measurement_sys; // 3255
	int16_t impulse_signal_polarity; // 3257
	int16_t vibratory_polarity_code; // 3259
	uint8_t unassigned[240];
	uint16_t revesion_number;
	int16_t fixed_length_trace_flag;
	int16_t extended_textual_header;
} SegyBinaryHeader;
#pragma pack(pop)

#pragma pack(push,1)
typedef struct {
	int32_t SEQWL; // 1
	int32_t SEQWR; // 5
	int32_t FFID; // 9
	int32_t TRCFLD; // 13
	int32_t SP; // 17
	int32_t CDP; // 21
	int16_t TRCNUM; // 25
	int16_t TRCID; // 29
	int16_t NVST; // 31
	int16_t NHST; // 33
	int16_t DU; //35
	int32_t DSREG; // 37
	int32_t REG; // 41
	int32_t SES; //45
	int32_t SDBS; // 49
	int32_t DERG; //53
	int32_t DES; //57
	int32_t WDS; //61
	int32_t WDG; // 65
	int16_t SAED; //69
	int16_t SAC; // 71
	int32_t SRCX; // 73
	int32_t SRCY; // 77
	int32_t GRPX; // 81
	int32_t GRPY; //85
	int16_t UNITS; // 89
	int16_t WVLE; // 91
	int16_t SBEL; // 93 
	int16_t UTSRC; // 95
	int16_t UTGRP; // 97
	int16_t SECSCOR; // 99
	int16_t GGRPCOR; // 101
	int16_t TSA; // 103
	int16_t LAGTA; // 105
	int16_t LAGTB; // 107
	int16_t DELRECT; // 109
	int16_t MTSTART; // 111
	int16_t MTEND; // 113
	int16_t NNSMP; // 115
	int16_t ST; // 117
	int16_t GTFI; // 119
	int16_t IG; // 121
	int16_t IGC; // 123
	int16_t CORREL; // 125
	int16_t SFSTART; // 127
	int16_t SFEND; // 129
	int16_t SLEN; // 131
	int16_t STYP; // 133
	int16_t SSTRLS; // 135
	int16_t SSTLE; // 137
	int16_t TTYP; // 139
	int16_t AFF; // 141
	int16_t AFS; // 143
	int16_t NFF; // 145
	int16_t NFS; //147
	int16_t LOCF; // 149
	int16_t HOCF; // 151
	int16_t LOCS; // 153
	int16_t HICS; // 155
	int16_t YEAR; // 157
	int16_t DAY; // 159
	int16_t HOUR; // 161
	int16_t MINUTE; // 163
	int16_t SCE; // 165
	int16_t TMBS; // 167
	int16_t TWF; // 169
	int16_t GGNSW; // 171
	int16_t GGNIST; // 173
	int16_t GGNLST; // 175
	int16_t GAPSZ; //177
	int16_t OAWT; // 179
	int32_t CDP_X; // 181
	int32_t CDP_Y; // 185
	int32_t INLINE; // 189
	int32_t XLINE; // 193
	int32_t SPN; // 197
	int16_t SPS; // 201
	int16_t TVMU; // 203
	uint8_t TC[6]; // 205
	int16_t TUNIT; // 211
	int16_t DTID; // 213
	int16_t SATS; // 215
	int16_t SRCTYP; // 217
	int32_t SEDSO; // 219
	uint8_t SRCM[6]; // 225
	int16_t SRCMU; //231;
} SegyTrace;
#pragma pack(pop)