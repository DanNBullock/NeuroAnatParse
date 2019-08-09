#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:57:48 2019

@author: dnbulloc
"""
import dipy
import dipy.tracking as dipytracking
import numpy as np
import nibabel as nib
import scipy.io as sio
import requests
import dipy.tracking.streamline as dts
def parse_mat_classification(classification):
    #if you understand mat objects in python and indexing, feel free to improve
    classificationObj=sio.loadmat(classification)
    classificationStruc=classificationObj['classification']
    classificationNamesField=tractNamesRawMat['names']
    namesStruc=classificationNamesField[0,0]
    namesShape=namesStruc.shape
    namesList = []
    for i in range(namesShape[1]):
        namesList.append('0') 
    for iNames in range(namesShape[1]):
        #namesList[iNames]=str(namesStruc[0,iNames]).replace('[\'', '').replace('\']', '')
        namesList[iNames]=namesStruc[0,iNames][0]
    classificationIndexField=tractNamesRawMat['index']
    index=classificationIndexField[0][0][0]
    return namesList,index;

def extract_subtract_from_tractome(selection,classification,tractome):
    namesList,index=parse_mat_classification(classification)
    if isinstance(selection, str):
        #be sure to account for 0 indexing
        nameIndex=namesList.index(selection)+1
        indexBool=index==nameIndex
        streamIndexes=[i for i, x in enumerate(indexBool) if x]
        
    elif isinstance(selection, int):
        indexBool=index==selection
        streamIndexes=[i for i, x in enumerate(indexBool) if x]
        
    streamsObjIN=nib.streamlines.load(tractome)
    #this doesn't work
    reorientedStreams=dts.orient_by_streamline(streamsObjIN.tractogram.streamlines[streamIndexes],streamsObjIN.tractogram.streamlines[streamIndexes[0]])
    sub_tractogram=nib.streamlines.Tractogram(reorientedStreams)
    #is it getting the appropriate header info?
    #sub_tractogram_reoriented=dipy.tracking.streamline.orient_by_streamline(sub_tractogram,sub_tractogram.tractogram.streamlines[0])
    modded_tractogram=nib.streamlines.tck.TckFile(sub_tractogram, nib.streamlines.header)
    
    return modded_tractogram

def create_tract_endpoint_mask(selection,classification,tractome,reference_image):
    ref_nifti=nib.load(reference_image)
    tractogram_out=extract_subtract_from_tractome(selection,classification,tractome)
    streamlinesIn=tractogram_out.tractogram.streamlines;
    tractogram_size=len(streamlinesIn._lengths)
    streamlines_endpoint_cluster_1=[ [] for i in range(tractogram_size) ]
    streamlines_endpoint_cluster_2=[ [] for i in range(tractogram_size) ]
    cluster_1_xvals=np.zeros(tractogram_size)
    cluster_1_yvals=np.zeros(tractogram_size)
    cluster_1_zvals=np.zeros(tractogram_size)
    cluster_2_xvals=np.zeros(tractogram_size)
    cluster_2_yvals=np.zeros(tractogram_size)
    cluster_2_zvals=np.zeros(tractogram_size)
    for iStreams in range(tractogram_size):
        streamlines_endpoint_cluster_1[iStreams]=np.delete(streamlinesIn[iStreams],range(1,len(streamlinesIn[iStreams])),axis=0)
        cluster_1_xvals[iStreams]=streamlines_endpoint_cluster_1[iStreams][0,0]
        cluster_1_yvals[iStreams]=streamlines_endpoint_cluster_1[iStreams][0,1]
        cluster_1_zvals[iStreams]=streamlines_endpoint_cluster_1[iStreams][0,2]
        streamlines_endpoint_cluster_2[iStreams]=np.delete(streamlinesIn[iStreams],range(0,len(streamlinesIn[iStreams])-1),axis=0)
        cluster_2_xvals[iStreams]=streamlines_endpoint_cluster_2[iStreams][0,0]
        cluster_2_yvals[iStreams]=streamlines_endpoint_cluster_2[iStreams][0,1]
        cluster_2_zvals[iStreams]=streamlines_endpoint_cluster_2[iStreams][0,2]
        
    cluster_1_centroid=[np.mean(cluster_1_xvals) ,np.mean(cluster_1_yvals), np.mean(cluster_1_zvals)]
    cluster_2_centroid=[np.mean(cluster_2_xvals) ,np.mean(cluster_2_yvals), np.mean(cluster_2_zvals)]
    displacement_vec=np.subtract(cluster_1_centroid, cluster_2_centroid)
    displacement_dim= np.argmax(displacement_vec)
    
    cluster_1_tractogram=nib.streamlines.Tractogram(streamlines_endpoint_cluster_1)
    cluster_2_tractogram=nib.streamlines.Tractogram(streamlines_endpoint_cluster_2)
    
    cluster_1_density_map = dipy.tracking.utils.density_map(streamlines_endpoint_cluster_1, ref_nifti.affine, ref_nifti.shape)
    cluster_2_density_map = dipy.tracking.utils.density_map(streamlines_endpoint_cluster_2, ref_nifti.affine, ref_nifti.shape)
   
    #RAS, LPI huristic
    
    if cluster_1_centroid[displacement_dim]>cluster_2_centroid[displacement_dim]:
        ras_nifti_out=nib.Nifti1Image(cluster_1_density_map.astype("int16"), ref_nifti.affine)
        lpi_nifti_out=nib.Nifti1Image(cluster_2_density_map.astype("int16"), ref_nifti.affine)
    elif cluster_1_centroid[displacement_dim]<cluster_2_centroid[displacement_dim]:
        ras_nifti_out=nib.Nifti1Image(cluster_2_density_map.astype("int16"), ref_nifti.affine)
        lpi_nifti_out=nib.Nifti1Image(cluster_1_density_map.astype("int16"), ref_nifti.affine)
        
    return ras_nifti_out, lpi_nifti_out

def decode_density_map_neurosynth(niftiIN):
    #THIS WILL ONLY RETURN SENSIBLE RESULTS IF YOUR NIFTI HAS BEEN WARPED TO MNI SPACE
    nifti_to_decode=nib.load(niftiIN)
    nifti_affine=nifti_to_decode.affine
    nifti_data=nifti_to_decode.get_data()
    #set and apply threshold
    threshold_density=100
    sub_threshold_indices = nifti_data < threshold_density
    nifti_data[sub_threshold_indices] = 0
    non_zero_indexes=np.where(nifti_data)
    non_zero_indexes_array=np.asarray(non_zero_indexes)
    #does the array need to be transposed?
    non_zero_indexes_array_transposed=np.transpose(non_zero_indexes_array)
    mni_coords= nib.affines.apply_affine(nifti_affine,non_zero_indexes_array_transposed)
    
    for iCoords in range(len(mni_coords)):
        coordstring=str(int(mni_coords[iCoords,0]))+'_'+str(int(mni_coords[iCoords,1]))+'_'+str(int(mni_coords[iCoords,2]))
        url_to_query='http://neurosynth.org/api/locations/'+coordstring+'/compare/'
        coord_json_results=requests.get(url_to_query).json()
        outArray=coord_json_results.get('data')
        blank_z_score_vec=zeros(len(outArray))
        #find clever way to iterate through features returned from json and sum z scores        
        for i
        outArray[:,1]
    
    
    

    
    
        #endpoints1.append(streamlinesIn[iStreams][0,0:3])
        #endpoints2.append(streamlinesIn[iStreams][-1,0:3])
      
    
   
    

    
    
        
    
    

def make_fgs_from_classification(classification,tractome):

    

# make fgs from classification
#iterate through fgs to make endpoint masks
#use masks to get functional mappings from  nimare
#WILL PROBABLY NEED TO BUILD CORPUS FOR THIS
    
#read in text and clean
#generate co-occurance matrix with structures
#generate co-occurance matrix with functions
#convert structures to coordnaites, and then pass to functions from nimare
#OPTIONAL: use parcellations to map cortical synonomy
#
    