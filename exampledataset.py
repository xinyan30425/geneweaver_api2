try:
    from geneweaver.client.datasets.nci60 import DNACombinedaCGHGeneSummary

    # Initializing the dataset will download the required data from nci.nih.gov
    ds = DNACombinedaCGHGeneSummary()

    # Use the LINKOUT attribute to get a link to the original data download page
    print(ds.LINKOUT)

    # Explore The Dataset
    # Gene Identifiers
    print(ds.gene_names[:5])
    print(ds.entrez_ids[:5])

    # Intensity Values
    intensity = ds.intensity.transpose()
    print(intensity[:10])

except Exception as e:
    print(f"An error occurred: {e}")
